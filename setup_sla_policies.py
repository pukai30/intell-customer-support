"""
Setup default SLA policies and templates for IT Support
Industry-standard SLA configurations
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.database import db_manager, SLAPolicy, SLATemplate, BusinessHours, Holiday, SLAEscalationRule
from datetime import datetime

# Industry-Standard SLA Policies
SLA_POLICIES = [
    # Critical/Urgent Priority
    {
        "policy_id": "IT_CRITICAL_247",
        "name": "Critical Issues - 24/7",
        "description": "For critical system outages and security breaches affecting multiple users",
        "domain": "IT",
        "categories": ["outage", "security", "data-loss"],
        "priorities": ["urgent", "critical"],
        "customer_tiers": ["standard", "premium", "vip"],
        "response_time_minutes": 15,  # 15 minutes
        "resolution_time_minutes": 60,  # 1 hour
        "use_business_hours": False,  # 24/7 coverage
        "auto_escalate": True,
        "is_default": False,
        "priority_order": 100,
        "escalation_rules": [
            {"level": 1, "trigger_after_minutes": 10, "escalate_to_tier": 1, "notify_emails": []},
            {"level": 2, "trigger_after_minutes": 30, "escalate_to_tier": 2, "notify_emails": []},
            {"level": 3, "trigger_after_minutes": 50, "escalate_to_tier": 3, "notify_emails": []}
        ]
    },
    
    # High Priority
    {
        "policy_id": "IT_HIGH_BUSINESS_HOURS",
        "name": "High Priority - Business Hours",
        "description": "Significant impact on productivity, single user affected",
        "domain": "IT",
        "categories": ["hardware", "software", "network", "email"],
        "priorities": ["high"],
        "customer_tiers": ["standard", "premium", "vip"],
        "response_time_minutes": 30,  # 30 minutes
        "resolution_time_minutes": 240,  # 4 hours
        "use_business_hours": True,
        "auto_escalate": True,
        "is_default": False,
        "priority_order": 80,
        "escalation_rules": [
            {"level": 1, "trigger_after_minutes": 120, "escalate_to_tier": 1, "notify_emails": []},
            {"level": 2, "trigger_after_minutes": 180, "escalate_to_tier": 2, "notify_emails": []}
        ]
    },
    
    # Medium Priority (Default)
    {
        "policy_id": "IT_MEDIUM_STANDARD",
        "name": "Medium Priority - Standard SLA",
        "description": "Standard support requests and general inquiries",
        "domain": "IT",
        "categories": ["password", "account", "access", "general"],
        "priorities": ["medium"],
        "customer_tiers": ["standard"],
        "response_time_minutes": 120,  # 2 hours
        "resolution_time_minutes": 480,  # 8 hours (1 business day)
        "use_business_hours": True,
        "auto_escalate": True,
        "is_default": True,  # This is the default policy
        "priority_order": 50,
        "escalation_rules": [
            {"level": 1, "trigger_after_minutes": 360, "escalate_to_tier": 1, "notify_emails": []}
        ]
    },
    
    # Low Priority
    {
        "policy_id": "IT_LOW_REQUESTS",
        "name": "Low Priority - Feature Requests",
        "description": "Feature requests, enhancements, and non-urgent questions",
        "domain": "IT",
        "categories": ["feature-request", "enhancement", "question"],
        "priorities": ["low"],
        "customer_tiers": ["standard", "premium", "vip"],
        "response_time_minutes": 480,  # 8 hours
        "resolution_time_minutes": 1920,  # 40 hours (5 business days)
        "use_business_hours": True,
        "auto_escalate": False,
        "is_default": False,
        "priority_order": 20,
        "escalation_rules": []
    },
    
    # VIP Customer - Expedited SLA
    {
        "policy_id": "IT_VIP_EXPEDITED",
        "name": "VIP Customer - Expedited Support",
        "description": "Priority support for VIP customers",
        "domain": "IT",
        "categories": [],  # Applies to all categories
        "priorities": ["medium", "high", "urgent"],
        "customer_tiers": ["vip"],
        "response_time_minutes": 15,  # 15 minutes
        "resolution_time_minutes": 120,  # 2 hours
        "use_business_hours": False,  # 24/7 for VIPs
        "auto_escalate": True,
        "is_default": False,
        "priority_order": 90,  # High priority, but lower than critical
        "escalation_rules": [
            {"level": 1, "trigger_after_minutes": 60, "escalate_to_tier": 1, "notify_emails": []},
            {"level": 2, "trigger_after_minutes": 100, "escalate_to_tier": 2, "notify_emails": []}
        ]
    },
    
    # Network Issues - Special SLA
    {
        "policy_id": "IT_NETWORK_URGENT",
        "name": "Network Issues - Urgent Response",
        "description": "Network connectivity and infrastructure issues",
        "domain": "IT",
        "categories": ["network", "connectivity", "vpn", "wifi"],
        "priorities": ["high", "urgent"],
        "customer_tiers": ["standard", "premium", "vip"],
        "response_time_minutes": 20,  # 20 minutes
        "resolution_time_minutes": 120,  # 2 hours
        "use_business_hours": False,  # Network issues can be 24/7
        "auto_escalate": True,
        "is_default": False,
        "priority_order": 85,
        "escalation_rules": [
            {"level": 1, "trigger_after_minutes": 60, "escalate_to_tier": 1, "notify_emails": []},
            {"level": 2, "trigger_after_minutes": 100, "escalate_to_tier": 2, "notify_emails": []}
        ]
    },
    
    # Security Issues - Immediate Response
    {
        "policy_id": "IT_SECURITY_IMMEDIATE",
        "name": "Security Issues - Immediate Response",
        "description": "Security incidents, breaches, and suspicious activity",
        "domain": "IT",
        "categories": ["security", "breach", "malware", "phishing"],
        "priorities": ["urgent", "critical"],
        "customer_tiers": ["standard", "premium", "vip"],
        "response_time_minutes": 10,  # 10 minutes
        "resolution_time_minutes": 60,  # 1 hour
        "use_business_hours": False,  # Security is always 24/7
        "auto_escalate": True,
        "is_default": False,
        "priority_order": 110,  # Highest priority
        "escalation_rules": [
            {"level": 1, "trigger_after_minutes": 5, "escalate_to_tier": 2, "notify_emails": ["security@company.com"]},
            {"level": 2, "trigger_after_minutes": 30, "escalate_to_tier": 3, "notify_emails": ["security@company.com", "ciso@company.com"]}
        ]
    }
]

# SLA Templates for quick setup
SLA_TEMPLATES = [
    {
        "template_id": "STANDARD_IT_SUPPORT",
        "name": "Standard IT Support SLA",
        "description": "Industry-standard SLA configuration for IT support teams",
        "category": "IT",
        "policies": [
            SLA_POLICIES[0],  # Critical
            SLA_POLICIES[1],  # High
            SLA_POLICIES[2],  # Medium (default)
            SLA_POLICIES[3]   # Low
        ]
    },
    {
        "template_id": "ENTERPRISE_IT_SLA",
        "name": "Enterprise IT Support with VIP",
        "description": "Enterprise-grade SLA with VIP customer support",
        "category": "IT",
        "policies": SLA_POLICIES  # All policies including VIP
    },
    {
        "template_id": "BASIC_IT_SUPPORT",
        "name": "Basic IT Support SLA",
        "description": "Simple SLA for small teams with business hours support",
        "category": "IT",
        "policies": [
            {
                "policy_id": "IT_BASIC_ALL",
                "name": "Basic IT Support - All Issues",
                "description": "Single SLA for all IT support requests",
                "domain": "IT",
                "categories": [],
                "priorities": [],
                "customer_tiers": ["standard"],
                "response_time_minutes": 240,  # 4 hours
                "resolution_time_minutes": 960,  # 2 business days
                "use_business_hours": True,
                "auto_escalate": False,
                "is_default": True,
                "priority_order": 50,
                "escalation_rules": []
            }
        ]
    }
]


async def setup_sla_policies():
    """Create default SLA policies and templates"""
    print("=" * 80)
    print("  SETTING UP SLA POLICIES & TEMPLATES")
    print("=" * 80)
    print()
    
    try:
        await db_manager.connect()
        
        # Create SLA Policies
        print("📋 Creating SLA Policies...")
        print("-" * 80)
        policy_success = 0
        policy_skip = 0
        
        for policy_data in SLA_POLICIES:
            try:
                # Check if policy exists
                existing = await db_manager.get_sla_policy(policy_data["policy_id"])
                if existing:
                    print(f"⚠️  Policy '{policy_data['name']}' already exists - skipping")
                    policy_skip += 1
                    continue
                
                # Build business hours
                bh = BusinessHours(
                    timezone="UTC",
                    working_days=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                    start_time="09:00",
                    end_time="17:00"
                )
                
                # Build escalation rules
                escalation_rules = [
                    SLAEscalationRule(**rule) for rule in policy_data.get("escalation_rules", [])
                ]
                
                policy = SLAPolicy(
                    policy_id=policy_data["policy_id"],
                    name=policy_data["name"],
                    description=policy_data["description"],
                    domain=policy_data["domain"],
                    categories=policy_data["categories"],
                    priorities=policy_data["priorities"],
                    customer_tiers=policy_data["customer_tiers"],
                    response_time_minutes=policy_data["response_time_minutes"],
                    resolution_time_minutes=policy_data["resolution_time_minutes"],
                    use_business_hours=policy_data["use_business_hours"],
                    business_hours=bh,
                    escalation_rules=escalation_rules,
                    auto_escalate=policy_data["auto_escalate"],
                    is_default=policy_data["is_default"],
                    priority_order=policy_data["priority_order"],
                    created_by="system"
                )
                
                await db_manager.create_sla_policy(policy)
                print(f"✅ Created: {policy_data['name']}")
                print(f"   → Response: {policy_data['response_time_minutes']}min, Resolution: {policy_data['resolution_time_minutes']}min")
                policy_success += 1
                
            except Exception as e:
                print(f"❌ Error creating policy {policy_data['name']}: {e}")
        
        print()
        print("📑 Creating SLA Templates...")
        print("-" * 80)
        template_success = 0
        template_skip = 0
        
        for template_data in SLA_TEMPLATES:
            try:
                # Check if template exists
                existing = await db_manager.get_sla_template(template_data["template_id"])
                if existing:
                    print(f"⚠️  Template '{template_data['name']}' already exists - skipping")
                    template_skip += 1
                    continue
                
                template = SLATemplate(
                    template_id=template_data["template_id"],
                    name=template_data["name"],
                    description=template_data["description"],
                    category=template_data["category"],
                    policies=template_data["policies"]
                )
                
                await db_manager.create_sla_template(template)
                print(f"✅ Created: {template_data['name']}")
                print(f"   → {len(template_data['policies'])} policies included")
                template_success += 1
                
            except Exception as e:
                print(f"❌ Error creating template {template_data['name']}: {e}")
        
        print()
        print("=" * 80)
        print(f"✅ SLA Setup Complete!")
        print(f"   - Policies Created: {policy_success} (Skipped: {policy_skip})")
        print(f"   - Templates Created: {template_success} (Skipped: {template_skip})")
        print("=" * 80)
        print()
        print("📊 Policy Summary:")
        print("   - Critical Issues (24/7): 15min response, 1hr resolution")
        print("   - High Priority: 30min response, 4hr resolution")
        print("   - Medium (Default): 2hr response, 8hr resolution")
        print("   - Low Priority: 8hr response, 5 days resolution")
        print("   - VIP Customers: 15min response, 2hr resolution (24/7)")
        print("   - Network Issues: 20min response, 2hr resolution")
        print("   - Security: 10min response, 1hr resolution (HIGHEST)")
        print()
        print("🎯 Templates Available:")
        print("   - STANDARD_IT_SUPPORT: Basic 4-tier SLA")
        print("   - ENTERPRISE_IT_SLA: Full featured with VIP support")
        print("   - BASIC_IT_SUPPORT: Simple single-tier SLA")
        print()
        
        await db_manager.disconnect()
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(setup_sla_policies())

