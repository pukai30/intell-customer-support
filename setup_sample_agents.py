"""
Setup Sample Support Agents
Run this script to populate the database with sample agents for testing
"""
import requests
import json

API_URL = "http://localhost:8000"

# Sample support agents with different skills
sample_agents = [
    {
        "agent_id": "AGENT-001",
        "name": "Sarah Johnson",
        "email": "sarah.johnson@company.com",
        "skills": ["password", "email", "security"],
        "skill_levels": {
            "password": "expert",
            "email": "expert",
            "security": "intermediate"
        },
        "max_concurrent_tickets": 15,
        "channels": ["email", "chat", "sms"],
        "shift_start": "08:00",
        "shift_end": "16:00",
        "timezone": "UTC"
    },
    {
        "agent_id": "AGENT-002",
        "name": "Michael Chen",
        "email": "michael.chen@company.com",
        "skills": ["vpn", "network", "hardware"],
        "skill_levels": {
            "vpn": "expert",
            "network": "expert",
            "hardware": "intermediate"
        },
        "max_concurrent_tickets": 12,
        "channels": ["email", "chat"],
        "shift_start": "09:00",
        "shift_end": "17:00",
        "timezone": "UTC"
    },
    {
        "agent_id": "AGENT-003",
        "name": "Emily Rodriguez",
        "email": "emily.rodriguez@company.com",
        "skills": ["software", "email", "mobile"],
        "skill_levels": {
            "software": "expert",
            "email": "intermediate",
            "mobile": "expert"
        },
        "max_concurrent_tickets": 10,
        "channels": ["email", "sms", "whatsapp", "chat"],
        "shift_start": "10:00",
        "shift_end": "18:00",
        "timezone": "UTC"
    },
    {
        "agent_id": "AGENT-004",
        "name": "David Kim",
        "email": "david.kim@company.com",
        "skills": ["hardware", "performance", "network"],
        "skill_levels": {
            "hardware": "expert",
            "performance": "expert",
            "network": "intermediate"
        },
        "max_concurrent_tickets": 10,
        "channels": ["email", "chat"],
        "shift_start": "07:00",
        "shift_end": "15:00",
        "timezone": "UTC"
    },
    {
        "agent_id": "AGENT-005",
        "name": "Jessica Brown",
        "email": "jessica.brown@company.com",
        "skills": ["password", "security", "database"],
        "skill_levels": {
            "password": "intermediate",
            "security": "expert",
            "database": "intermediate"
        },
        "max_concurrent_tickets": 8,
        "channels": ["email", "chat"],
        "shift_start": "12:00",
        "shift_end": "20:00",
        "timezone": "UTC"
    },
    {
        "agent_id": "AGENT-006",
        "name": "Robert Martinez",
        "email": "robert.martinez@company.com",
        "skills": ["vpn", "email", "software", "network"],
        "skill_levels": {
            "vpn": "intermediate",
            "email": "intermediate",
            "software": "intermediate",
            "network": "intermediate"
        },
        "max_concurrent_tickets": 12,
        "channels": ["email", "sms", "whatsapp", "chat"],
        "shift_start": "08:30",
        "shift_end": "16:30",
        "timezone": "UTC"
    },
    {
        "agent_id": "AGENT-007",
        "name": "Amanda Wilson",
        "email": "amanda.wilson@company.com",
        "skills": ["mobile", "software", "email"],
        "skill_levels": {
            "mobile": "expert",
            "software": "intermediate",
            "email": "beginner"
        },
        "max_concurrent_tickets": 10,
        "channels": ["email", "whatsapp", "sms"],
        "shift_start": "11:00",
        "shift_end": "19:00",
        "timezone": "UTC"
    },
    {
        "agent_id": "AGENT-008",
        "name": "Thomas Anderson",
        "email": "thomas.anderson@company.com",
        "skills": ["hardware", "network", "vpn", "performance"],
        "skill_levels": {
            "hardware": "expert",
            "network": "expert",
            "vpn": "intermediate",
            "performance": "intermediate"
        },
        "max_concurrent_tickets": 15,
        "channels": ["email", "chat"],
        "shift_start": "06:00",
        "shift_end": "14:00",
        "timezone": "UTC"
    }
]


def create_agents():
    """Create sample agents in the database"""
    print("=" * 80)
    print("  CREATING SAMPLE SUPPORT AGENTS")
    print("=" * 80)
    print(f"API URL: {API_URL}")
    print(f"Total agents to create: {len(sample_agents)}")
    print("-" * 80)
    print()
    
    created_count = 0
    failed_count = 0
    failed_agents = []
    
    for idx, agent_data in enumerate(sample_agents, 1):
        print(f"[{idx}/{len(sample_agents)}] Creating: {agent_data['name']}")
        print(f"  Agent ID: {agent_data['agent_id']}")
        print(f"  Email: {agent_data['email']}")
        print(f"  Skills: {', '.join(agent_data['skills'])}")
        print(f"  Max tickets: {agent_data['max_concurrent_tickets']}")
        print(f"  Channels: {', '.join(agent_data['channels'])}")
        
        try:
            response = requests.post(
                f"{API_URL}/api/agents/create",
                json=agent_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✓ Success: {result['message']}")
                created_count += 1
            else:
                error_detail = response.json().get("detail", "Unknown error")
                print(f"  ✗ Failed: {response.status_code} - {error_detail}")
                failed_count += 1
                failed_agents.append(agent_data['name'])
        
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            failed_count += 1
            failed_agents.append(agent_data['name'])
        
        print()
    
    # Summary
    print("=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    print(f"✓ Successfully created: {created_count}/{len(sample_agents)} agents")
    
    if failed_count > 0:
        print(f"\n✗ Failed agents:")
        for agent_name in failed_agents:
            print(f"  - {agent_name}")
    
    print("\n" + "-" * 80)
    print("Agent Skill Coverage:")
    print("-" * 80)
    
    # Calculate skill coverage
    skill_coverage = {}
    for agent in sample_agents:
        for skill in agent['skills']:
            if skill not in skill_coverage:
                skill_coverage[skill] = []
            skill_coverage[skill].append(agent['name'])
    
    for skill in sorted(skill_coverage.keys()):
        agents_with_skill = skill_coverage[skill]
        print(f"  - {skill.capitalize()}: {len(agents_with_skill)} agents")
        for agent in agents_with_skill:
            print(f"      • {agent}")
    
    print("\n" + "-" * 80)
    print("Quick Tips:")
    print("-" * 80)
    print("  - View all agents: GET http://localhost:8000/api/agents/list")
    print("  - View team stats: GET http://localhost:8000/api/agents/team/stats")
    print("  - View specific agent: GET http://localhost:8000/api/agents/{agent_id}")
    print("  - Toggle agent status: PUT http://localhost:8000/api/agents/{agent_id}/status?is_active=true")
    print()
    print("  - Test auto-assignment by sending a test email:")
    print("    Subject: 'I forgot my password'")
    print("    → Should auto-assign to Sarah Johnson (password expert)")
    print()
    print("    Subject: 'VPN not connecting'")
    print("    → Should auto-assign to Michael Chen or Thomas Anderson (VPN experts)")
    print()
    print("=" * 80)


if __name__ == "__main__":
    create_agents()

