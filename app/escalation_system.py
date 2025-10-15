"""
SLA Monitoring and Automatic Escalation System
Monitors ticket SLAs and escalates to higher-tier agents when needed
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from app.database import db_manager, SupportTicket, Agent
from app.skill_mapper import skill_mapper


class EscalationSystem:
    """Handles SLA monitoring and automatic ticket escalation"""
    
    async def check_and_escalate_tickets(self):
        """Check for SLA breaches and escalate tickets"""
        now = datetime.utcnow()
        escalated_count = 0
        
        # Find all tickets that need escalation
        tickets_to_check = await db_manager.get_all_tickets()
        
        for ticket in tickets_to_check:
            # Skip if already resolved or closed
            if ticket.status in ["resolved", "closed"]:
                continue
            
            should_escalate = False
            reason = ""
            
            # Check response SLA
            if (ticket.sla_response_deadline and 
                not ticket.first_response_at and 
                now > ticket.sla_response_deadline):
                should_escalate = True
                reason = "Response SLA breached"
                ticket.sla_response_breached = True
            
            # Check resolution SLA
            elif (ticket.sla_resolution_deadline and 
                  not ticket.resolved_at and 
                  now > ticket.sla_resolution_deadline):
                should_escalate = True
                reason = "Resolution SLA breached"
                ticket.sla_resolution_breached = True
            
            # Escalate if needed
            if should_escalate:
                result = await self.escalate_ticket(ticket, reason)
                if result:
                    escalated_count += 1
                    print(f"⚠️  Escalated ticket {ticket.ticket_id}: {reason}")
        
        if escalated_count > 0:
            print(f"📈 Escalated {escalated_count} ticket(s) due to SLA breaches")
        
        return escalated_count
    
    async def escalate_ticket(
        self,
        ticket: SupportTicket,
        reason: str
    ) -> Optional[Dict[str, Any]]:
        """Escalate a ticket to a higher-tier agent"""
        
        # Get current agent's tier
        current_tier = 0
        if ticket.assigned_to:
            current_agent = await db_manager.get_agent_by_email(ticket.assigned_to)
            if current_agent:
                current_tier = current_agent.tier
                # Decrement current agent's load
                await db_manager.decrement_agent_load(current_agent.agent_id)
        
        # Extract skills from ticket
        issue_analysis = skill_mapper.categorize_issue(
            f"{ticket.subject or ''} {ticket.conversation[0].content if ticket.conversation else ''}"
        )
        required_skills = issue_analysis["skills"]
        
        # Find higher-tier agent
        escalation_agent = await db_manager.get_escalation_agent(
            current_tier=current_tier,
            skills=required_skills,
            domain=ticket.support_domain
        )
        
        if not escalation_agent:
            # No higher-tier agent available
            await db_manager.update_ticket(ticket.ticket_id, {
                "status": "escalated",
                "priority": "urgent",  # Upgrade priority
                "sla_response_breached": ticket.sla_response_breached,
                "sla_resolution_breached": ticket.sla_resolution_breached
            })
            return None
        
        # Update ticket with escalation
        escalation_record = {
            "timestamp": datetime.utcnow(),
            "from_agent": ticket.assigned_to,
            "to_agent": escalation_agent.email,
            "from_tier": current_tier,
            "to_tier": escalation_agent.tier,
            "reason": reason
        }
        
        # Increment escalation level
        new_escalation_level = ticket.escalation_level + 1
        
        # Update ticket
        await db_manager.update_ticket(ticket.ticket_id, {
            "assigned_to": escalation_agent.email,
            "assigned_at": datetime.utcnow(),
            "escalation_level": new_escalation_level,
            "escalated_at": datetime.utcnow(),
            "escalated_to": escalation_agent.email,
            "$push": {"escalation_history": escalation_record},
            "status": "escalated",
            "priority": "high" if new_escalation_level == 1 else "urgent",
            "sla_response_breached": ticket.sla_response_breached,
            "sla_resolution_breached": ticket.sla_resolution_breached
        })
        
        # Increment new agent's load
        await db_manager.increment_agent_load(escalation_agent.agent_id)
        
        return {
            "escalated": True,
            "agent_name": escalation_agent.name,
            "agent_email": escalation_agent.email,
            "agent_tier": escalation_agent.tier,
            "escalation_level": new_escalation_level,
            "reason": reason
        }
    
    async def get_sla_dashboard(self) -> Dict[str, Any]:
        """Get SLA compliance dashboard metrics"""
        all_tickets = await db_manager.get_all_tickets()
        
        total_tickets = len(all_tickets)
        response_breaches = sum(1 for t in all_tickets if t.sla_response_breached)
        resolution_breaches = sum(1 for t in all_tickets if t.sla_resolution_breached)
        escalated = sum(1 for t in all_tickets if t.escalation_level > 0)
        
        # Calculate average response time
        response_times = []
        for ticket in all_tickets:
            if ticket.first_response_at and ticket.created_at:
                response_time = (ticket.first_response_at - ticket.created_at).total_seconds() / 60
                response_times.append(response_time)
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        # Calculate SLA compliance rates
        response_compliance = ((total_tickets - response_breaches) / total_tickets * 100) if total_tickets > 0 else 100
        resolution_compliance = ((total_tickets - resolution_breaches) / total_tickets * 100) if total_tickets > 0 else 100
        
        return {
            "total_tickets": total_tickets,
            "response_sla_breaches": response_breaches,
            "resolution_sla_breaches": resolution_breaches,
            "escalated_tickets": escalated,
            "response_compliance_rate": round(response_compliance, 2),
            "resolution_compliance_rate": round(resolution_compliance, 2),
            "avg_response_time_minutes": round(avg_response_time, 2),
            "tickets_by_escalation_level": {
                "L0": sum(1 for t in all_tickets if t.escalation_level == 0),
                "L1": sum(1 for t in all_tickets if t.escalation_level == 1),
                "L2": sum(1 for t in all_tickets if t.escalation_level == 2),
                "L3": sum(1 for t in all_tickets if t.escalation_level >= 3)
            }
        }


# Global escalation system instance
escalation_system = EscalationSystem()

