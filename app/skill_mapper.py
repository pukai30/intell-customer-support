"""
Skill Mapping System for Intelligent Ticket Assignment
Maps ticket content to agent skills for optimal routing
"""
from typing import List, Dict, Set
import re


class SkillMapper:
    """Maps ticket content to required skills"""
    
    # Skill categories with keywords
    SKILL_KEYWORDS = {
        "password": [
            "password", "passwd", "login", "sign in", "authentication",
            "credentials", "forgot password", "reset password", "locked account",
            "unlock", "access denied"
        ],
        "email": [
            "email", "outlook", "mail", "inbox", "send", "receive",
            "attachment", "spam", "calendar", "meeting invite", "distribution list"
        ],
        "vpn": [
            "vpn", "remote access", "work from home", "wfh", "connection",
            "remote desktop", "rdp", "citrix", "tunnel"
        ],
        "hardware": [
            "computer", "laptop", "desktop", "monitor", "keyboard", "mouse",
            "printer", "scanner", "dock", "station", "usb", "screen",
            "power", "battery", "charger", "display"
        ],
        "network": [
            "network", "internet", "wifi", "wi-fi", "ethernet", "connection",
            "slow", "cannot connect", "no internet", "dns", "ip address",
            "network drive", "shared folder", "file server"
        ],
        "software": [
            "software", "application", "app", "program", "install", "uninstall",
            "update", "upgrade", "license", "microsoft office", "teams",
            "zoom", "adobe", "chrome", "browser"
        ],
        "security": [
            "security", "virus", "malware", "phishing", "spam", "suspicious",
            "antivirus", "firewall", "threat", "breach", "hack", "encryption",
            "2fa", "two factor", "mfa", "multi-factor"
        ],
        "mobile": [
            "mobile", "phone", "iphone", "android", "smartphone", "tablet",
            "ipad", "byod", "mobile device", "mdm", "activesync"
        ],
        "database": [
            "database", "sql", "query", "data", "oracle", "mysql",
            "access denied", "permission", "report", "crystal reports"
        ],
        "performance": [
            "slow", "frozen", "freeze", "crash", "hang", "not responding",
            "performance", "speed", "lag", "stuck"
        ]
    }
    
    # Skill priorities (higher = more critical)
    SKILL_PRIORITIES = {
        "security": 10,
        "password": 8,
        "vpn": 7,
        "network": 6,
        "email": 5,
        "hardware": 4,
        "software": 3,
        "performance": 2,
        "mobile": 2,
        "database": 1
    }
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract required skills from ticket text
        
        Args:
            text: Ticket content (subject + body)
        
        Returns:
            List of skill categories sorted by relevance
        """
        if not text:
            return []
        
        text_lower = text.lower()
        skill_scores: Dict[str, float] = {}
        
        # Score each skill based on keyword matches
        for skill, keywords in self.SKILL_KEYWORDS.items():
            score = 0.0
            for keyword in keywords:
                # Use word boundaries for exact matches
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, text_lower))
                if matches > 0:
                    # Weight by keyword specificity (longer keywords = more specific)
                    keyword_weight = len(keyword) / 10.0
                    score += matches * keyword_weight
            
            if score > 0:
                # Apply priority multiplier
                priority = self.SKILL_PRIORITIES.get(skill, 1)
                skill_scores[skill] = score * priority
        
        # Sort skills by score (descending)
        sorted_skills = sorted(
            skill_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        # Return top skills (threshold: at least 10% of top score)
        if sorted_skills:
            top_score = sorted_skills[0][1]
            threshold = top_score * 0.1
            return [skill for skill, score in sorted_skills if score >= threshold]
        
        return []
    
    def categorize_ticket(self, subject: str, body: str) -> Dict[str, any]:
        """
        Categorize a ticket and extract metadata
        
        Args:
            subject: Ticket subject
            body: Ticket body
        
        Returns:
            Dictionary with skills, category, and priority
        """
        combined_text = f"{subject} {body}"
        skills = self.extract_skills(combined_text)
        
        # Determine primary category (first skill)
        primary_category = skills[0] if skills else "general"
        
        # Determine priority based on urgency keywords
        priority = self._detect_priority(combined_text)
        
        return {
            "skills": skills,
            "primary_category": primary_category,
            "priority": priority,
            "is_urgent": priority in ["high", "urgent"]
        }
    
    def _detect_priority(self, text: str) -> str:
        """Detect priority level from text"""
        text_lower = text.lower()
        
        # Urgent keywords
        urgent_keywords = [
            "urgent", "emergency", "critical", "asap", "immediately",
            "down", "outage", "can't work", "cannot work", "production"
        ]
        
        # High priority keywords
        high_keywords = [
            "important", "soon", "quickly", "priority", "need help"
        ]
        
        for keyword in urgent_keywords:
            if keyword in text_lower:
                return "urgent"
        
        for keyword in high_keywords:
            if keyword in text_lower:
                return "high"
        
        return "medium"
    
    def match_agent_skills(self, required_skills: List[str], agent_skills: List[str]) -> float:
        """
        Calculate skill match score between required and agent skills
        
        Args:
            required_skills: Skills needed for ticket
            agent_skills: Skills possessed by agent
        
        Returns:
            Match score (0.0 to 1.0)
        """
        if not required_skills:
            return 0.5  # Neutral score if no specific skills required
        
        if not agent_skills:
            return 0.0  # No match if agent has no skills
        
        required_set = set(required_skills)
        agent_set = set(agent_skills)
        
        # Calculate intersection
        matches = required_set & agent_set
        
        # Score based on percentage of required skills covered
        match_score = len(matches) / len(required_set)
        
        # Bonus if agent has all required skills
        if match_score == 1.0:
            match_score = 1.0
        
        return match_score


# Global skill mapper instance
skill_mapper = SkillMapper()

