"""
Intelligent Auto-Assignment System
Automatically assigns tickets to best available agents based on skills and workload
"""
from typing import Optional, Dict, List
from datetime import datetime
from app.database import db_manager, Agent, ConversationMessage
from app.skill_mapper import skill_mapper


class AutoAssignmentSystem:
    """Handles intelligent ticket assignment to agents"""
    
    async def auto_assign_ticket(
        self,
        ticket_id: str,
        subject: str,
        body: str,
        channel: str
    ) -> Optional[Dict[str, any]]:
        """
        Automatically assign a ticket to the best available agent
        
        Args:
            ticket_id: Ticket ID to assign
            subject: Ticket subject
            body: Ticket body/content
            channel: Communication channel (email, sms, whatsapp, chat)
        
        Returns:
            Assignment result with agent info, or None if no agent available
        """
        # 1. Analyze ticket to extract required skills
        ticket_analysis = skill_mapper.categorize_ticket(subject, body)
        required_skills = ticket_analysis["skills"]
        priority = ticket_analysis["priority"]
        
        print(f"🔍 Analyzing ticket {ticket_id}")
        print(f"   Required skills: {required_skills}")
        print(f"   Priority: {priority}")
        
        # 2. Find best available agent (MUST have matching skills, NO fallback)
        # Only assign if agent has the required skills
        available_agents = await db_manager.get_available_agents(
            skills=required_skills
        )
        
        # If no agents with matching skills, DO NOT assign - requires human assignment
        if not available_agents:
            print(f"⚠️  No agents found with required skills: {required_skills}")
            print(f"   → Ticket will be marked for manual/human assignment")
            return None
        
        # Find the best agent from available agents
        best_agent = None
        best_score = -1
        
        for agent in available_agents:
            # Calculate agent score based on skills and load
            skill_score = 0
            for skill in required_skills:
                if skill in agent.skills:
                    skill_level = agent.skill_levels.get(skill, "beginner")
                    level_scores = {"beginner": 1, "intermediate": 2, "advanced": 3, "expert": 4}
                    skill_score += level_scores.get(skill_level, 1)
            
            # Load factor (lower load = higher score)
            load_factor = 1 - (agent.current_load / agent.max_concurrent_tickets)
            
            # Tier factor (higher tier = higher score)
            tier_factor = agent.tier + 1
            
            # Channel preference
            channel_factor = 1.5 if channel in agent.channels else 1.0
            
            # Calculate total score
            total_score = (skill_score * 0.4 + load_factor * 0.3 + tier_factor * 0.2 + channel_factor * 0.1)
            
            if total_score > best_score:
                best_score = total_score
                best_agent = agent
        
        if not best_agent:
            print(f"⚠️  No available agent found for ticket {ticket_id}")
            return None
        
        print(f"✓ Best agent found: {best_agent.name} ({best_agent.email})")
        print(f"   Skills: {best_agent.skills}")
        print(f"   Current load: {best_agent.current_load}/{best_agent.max_concurrent_tickets}")
        print(f"   Agent score: {best_score:.2f}")
        
        # 3. Assign ticket to agent
        assignment_time = datetime.utcnow()
        
        # Update ticket
        await db_manager.update_ticket(ticket_id, {
            "assigned_to": best_agent.email,
            "assigned_at": assignment_time,
            "requires_human": False,  # Clear the flag once assigned
            "priority": priority,  # Update priority based on analysis
            "metadata": {
                "assigned_agent_id": best_agent.agent_id,
                "assigned_agent_name": best_agent.name,
                "required_skills": required_skills,
                "auto_assigned": True,
                "assignment_reason": self._get_assignment_reason(best_agent, required_skills)
            }
        })
        
        # Add system message to conversation
        system_message = ConversationMessage(
            role="system",
            content=self._create_assignment_message(best_agent, required_skills),
            metadata={
                "action": "auto_assignment",
                "agent_id": best_agent.agent_id,
                "agent_name": best_agent.name,
                "agent_email": best_agent.email,
                "required_skills": required_skills,
                "agent_skills": best_agent.skills
            }
        )
        await db_manager.add_message_to_ticket(ticket_id, system_message)
        
        # Increment agent's workload
        await db_manager.increment_agent_load(best_agent.agent_id)
        
        print(f"✓ Ticket {ticket_id} assigned to {best_agent.name}")
        
        return {
            "assigned": True,
            "agent_id": best_agent.agent_id,
            "agent_name": best_agent.name,
            "agent_email": best_agent.email,
            "agent_skills": best_agent.skills,
            "required_skills": required_skills,
            "priority": priority,
            "new_load": best_agent.current_load + 1
        }
    
    def _get_assignment_reason(self, agent: Agent, required_skills: List[str]) -> str:
        """Generate human-readable assignment reason"""
        if not required_skills:
            return f"Assigned to {agent.name} (least loaded agent)"
        
        # Check skill matches
        agent_skill_set = set(agent.skills)
        required_skill_set = set(required_skills)
        matched_skills = agent_skill_set & required_skill_set
        
        if matched_skills:
            skills_str = ", ".join(matched_skills)
            return f"Assigned to {agent.name} (expertise in: {skills_str})"
        else:
            return f"Assigned to {agent.name} (available agent)"
    
    def _create_assignment_message(self, agent: Agent, required_skills: List[str]) -> str:
        """Create assignment system message"""
        if required_skills:
            skills_str = ", ".join(required_skills)
            return f"🎯 Ticket automatically assigned to {agent.name} ({agent.email}) based on expertise in: {skills_str}. Current workload: {agent.current_load + 1}/{agent.max_concurrent_tickets} tickets."
        else:
            return f"🎯 Ticket automatically assigned to {agent.name} ({agent.email}). Current workload: {agent.current_load + 1}/{agent.max_concurrent_tickets} tickets."
    
    async def release_ticket(self, ticket_id: str, agent_id: str):
        """
        Release a ticket from an agent (when resolved/closed)
        
        Args:
            ticket_id: Ticket ID
            agent_id: Agent ID to release from
        """
        # Decrement agent's workload
        await db_manager.decrement_agent_load(agent_id)
        
        # Add system message
        agent = await db_manager.get_agent(agent_id)
        if agent:
            system_message = ConversationMessage(
                role="system",
                content=f"✓ Ticket resolved by {agent.name}. Agent's new workload: {agent.current_load}/{agent.max_concurrent_tickets} tickets.",
                metadata={
                    "action": "ticket_release",
                    "agent_id": agent_id,
                    "agent_name": agent.name
                }
            )
            await db_manager.add_message_to_ticket(ticket_id, system_message)
        
        print(f"✓ Ticket {ticket_id} released from agent {agent_id}")
    
    async def get_agent_stats(self, agent_id: str) -> Optional[Dict[str, any]]:
        """Get detailed statistics for an agent"""
        agent = await db_manager.get_agent(agent_id)
        if not agent:
            return None
        
        # Get agent's tickets
        all_tickets = await db_manager.get_all_tickets()
        agent_tickets = [
            t for t in all_tickets
            if t.assigned_to == agent.email
        ]
        
        # Calculate stats
        open_tickets = [t for t in agent_tickets if t.status in ["open", "pending"]]
        resolved_tickets = [t for t in agent_tickets if t.status in ["resolved", "closed"]]
        
        return {
            "agent_id": agent.agent_id,
            "name": agent.name,
            "email": agent.email,
            "skills": agent.skills,
            "is_active": agent.is_active,
            "current_load": agent.current_load,
            "max_concurrent_tickets": agent.max_concurrent_tickets,
            "utilization_percent": (agent.current_load / agent.max_concurrent_tickets * 100) if agent.max_concurrent_tickets > 0 else 0,
            "total_assigned": agent.total_assigned,
            "total_resolved": agent.total_resolved,
            "open_count": len(open_tickets),
            "resolved_count": len(resolved_tickets),
            "avg_resolution_time_minutes": agent.avg_resolution_time_minutes,
            "last_assigned_at": agent.last_assigned_at.isoformat() if agent.last_assigned_at else None,
            "open_ticket_ids": [t.ticket_id for t in open_tickets],
            "channels": agent.channels
        }
    
    async def get_team_stats(self) -> Dict[str, any]:
        """Get team-wide statistics"""
        agents = await db_manager.get_all_agents(active_only=False)
        all_tickets = await db_manager.get_all_tickets()
        
        if not agents:
            return {
                "total_agents": 0,
                "active_agents": 0,
                "total_capacity": 0,
                "total_load": 0,
                "team_utilization_percent": 0,
                "agents": []
            }
        
        # Recalculate and fix negative loads
        for agent in agents:
            agent_tickets = [
                t for t in all_tickets
                if t.assigned_to and t.assigned_to.strip().lower() == agent.email.strip().lower()
                and t.status in ["open", "in_progress", "pending"]
            ]
            actual_load = max(0, len(agent_tickets))  # Ensure non-negative
            
            if agent.current_load < 0 or agent.current_load != actual_load:
                await db_manager.update_agent(agent.agent_id, {"current_load": actual_load})
                agent.current_load = actual_load
        
        active_agents = [a for a in agents if a.is_active]
        total_capacity = sum(a.max_concurrent_tickets for a in active_agents)
        total_load = sum(max(0, a.current_load) for a in active_agents)
        
        # Get individual agent stats
        agent_stats = []
        for agent in agents:
            stats = await self.get_agent_stats(agent.agent_id)
            if stats:
                agent_stats.append(stats)
        
        return {
            "total_agents": len(agents),
            "active_agents": len(active_agents),
            "total_capacity": total_capacity,
            "total_load": total_load,
            "team_utilization_percent": (total_load / total_capacity * 100) if total_capacity > 0 else 0,
            "available_capacity": max(0, total_capacity - total_load),
            "agents": agent_stats,
            "top_performers": sorted(
                [a for a in agent_stats if a["total_resolved"] > 0],
                key=lambda x: x["total_resolved"],
                reverse=True
            )[:5]
        }


# Global auto-assignment system instance
auto_assignment = AutoAssignmentSystem()

