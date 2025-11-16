#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ethical Considerations Tracking Module for Gazzali Research

This module provides functionality to extract, track, and document ethical
considerations in academic research, including IRB approvals, informed consent,
privacy protections, and ethical safeguards.

Requirements addressed:
- 10.1: Identify ethical considerations in reviewed literature
- 10.2: Document ethical approval processes and IRB oversight
- 10.3: Highlight ethical safeguards in research involving human subjects, animals, or sensitive data
- 10.4: Identify potential ethical concerns or limitations
- 10.5: Generate ethics section in reports

Components:
- EthicsTracker: Main class for tracking ethical considerations
- EthicalConsideration: Data class for individual ethical considerations
- IRBApproval: Data class for IRB approval information
- EthicalSafeguard: Data class for ethical safeguards
"""

from __future__ import annotations

import re
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from enum import Enum


# Configure logging
logger = logging.getLogger(__name__)


class EthicsCategory(str, Enum):
    """Categories of ethical considerations"""
    INFORMED_CONSENT = "informed_consent"
    PRIVACY_PROTECTION = "privacy_protection"
    VULNERABLE_POPULATIONS = "vulnerable_populations"
    POTENTIAL_HARMS = "potential_harms"
    DATA_SECURITY = "data_security"
    ANIMAL_WELFARE = "animal_welfare"
    CONFLICT_OF_INTEREST = "conflict_of_interest"
    DECEPTION = "deception"
    CONFIDENTIALITY = "confidentiality"
    DUAL_USE = "dual_use"
    ENVIRONMENTAL_IMPACT = "environmental_impact"
    CULTURAL_SENSITIVITY = "cultural_sensitivity"
    OTHER = "other"


class ResearchSubjectType(str, Enum):
    """Types of research subjects"""
    HUMAN_SUBJECTS = "human_subjects"
    ANIMAL_SUBJECTS = "animal_subjects"
    SENSITIVE_DATA = "sensitive_data"
    NONE = "none"


@dataclass
class IRBApproval:
    """
    Information about Institutional Review Board (IRB) approval.
    
    Attributes:
        has_approval: Whether IRB approval was obtained
        irb_number: IRB approval number/identifier
        institution: Institution that provided approval
        approval_type: Type of approval (full review, expedited, exempt)
        details: Additional details about the approval
        confidence: Confidence in extraction (0-1)
    """
    has_approval: bool
    irb_number: str = ""
    institution: str = ""
    approval_type: str = ""
    details: str = ""
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "has_approval": self.has_approval,
            "irb_number": self.irb_number,
            "institution": self.institution,
            "approval_type": self.approval_type,
            "details": self.details,
            "confidence": self.confidence,
        }


@dataclass
class EthicalSafeguard:
    """
    Information about ethical safeguards implemented in research.
    
    Attributes:
        safeguard_type: Type of safeguard (e.g., "anonymization", "encryption")
        description: Description of the safeguard
        category: Ethical category this safeguard addresses
        effectiveness: Assessment of effectiveness
        confidence: Confidence in extraction (0-1)
    """
    safeguard_type: str
    description: str
    category: EthicsCategory
    effectiveness: str = ""
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "safeguard_type": self.safeguard_type,
            "description": self.description,
            "category": self.category.value,
            "effectiveness": self.effectiveness,
            "confidence": self.confidence,
        }


@dataclass
class EthicalConsideration:
    """
    Information about an ethical consideration in research.
    
    Attributes:
        category: Category of ethical consideration
        description: Description of the consideration
        severity: Severity level (low, moderate, high)
        addressed: Whether the consideration was addressed
        mitigation: How the concern was mitigated
        source_text: Original text mentioning this consideration
        confidence: Confidence in extraction (0-1)
    """
    category: EthicsCategory
    description: str
    severity: str = "moderate"
    addressed: bool = False
    mitigation: str = ""
    source_text: str = ""
    confidence: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "category": self.category.value,
            "description": self.description,
            "severity": self.severity,
            "addressed": self.addressed,
            "mitigation": self.mitigation,
            "source_text": self.source_text,
            "confidence": self.confidence,
        }


class EthicsTracker:
    """
    Tracks and extracts ethical considerations from academic research.
    
    This class analyzes research content to identify:
    - IRB approvals and ethical oversight
    - Informed consent procedures
    - Privacy and confidentiality protections
    - Vulnerable population considerations
    - Potential harms and risks
    - Ethical safeguards implemented
    - Ethical concerns and limitations
    """
    
    # IRB and ethics approval patterns
    IRB_PATTERNS = [
        r'\birb\b',
        r'\binstitutional review board\b',
        r'\bethics committee\b',
        r'\bethics approval\b',
        r'\bethical approval\b',
        r'\bethics review\b',
        r'\bapproved by.*ethics\b',
        r'\bapproval number\b',
        r'\bprotocol number\b',
        r'\birb\s*#?\s*\d+',
        r'\bexempt.*irb\b',
        r'\bexpedited.*review\b',
    ]
    
    # Informed consent patterns
    INFORMED_CONSENT_PATTERNS = [
        r'\binformed consent\b',
        r'\bwritten consent\b',
        r'\bverbal consent\b',
        r'\bconsent form\b',
        r'\bparticipants.*consented\b',
        r'\bvoluntary participation\b',
        r'\bright to withdraw\b',
        r'\bconsent process\b',
        r'\bconsent procedure\b',
    ]
    
    # Privacy and confidentiality patterns
    PRIVACY_PATTERNS = [
        r'\bprivacy\b',
        r'\bconfidentiality\b',
        r'\banonymity\b',
        r'\banonymized\b',
        r'\bde-identified\b',
        r'\bpseudonym',
        r'\bdata protection\b',
        r'\bsecure storage\b',
        r'\bencrypted\b',
        r'\bconfidential\b',
    ]
    
    # Vulnerable population patterns
    VULNERABLE_POPULATION_PATTERNS = [
        r'\bvulnerable population\b',
        r'\bchildren\b',
        r'\bminors\b',
        r'\bpregnant women\b',
        r'\bprisoners\b',
        r'\bcognitively impaired\b',
        r'\bmentally disabled\b',
        r'\beconomically disadvantaged\b',
        r'\brefugees\b',
        r'\bindigenous\b',
    ]
    
    # Potential harms patterns
    HARM_PATTERNS = [
        r'\bpotential harm\b',
        r'\brisk\b',
        r'\badverse effect\b',
        r'\bpsychological distress\b',
        r'\bemotional harm\b',
        r'\bphysical harm\b',
        r'\bsocial harm\b',
        r'\bstigma\b',
        r'\bdiscrimination\b',
    ]
    
    # Animal research patterns
    ANIMAL_PATTERNS = [
        r'\banimal\b',
        r'\bmice\b',
        r'\brats\b',
        r'\bprimates\b',
        r'\biacuc\b',
        r'\binstitutional animal care\b',
        r'\banimal welfare\b',
        r'\bhumane treatment\b',
        r'\beuthanasia\b',
    ]
    
    # Data security patterns
    DATA_SECURITY_PATTERNS = [
        r'\bdata security\b',
        r'\bsecure server\b',
        r'\bencryption\b',
        r'\bpassword protected\b',
        r'\baccess control\b',
        r'\bdata breach\b',
        r'\bgdpr\b',
        r'\bhipaa\b',
    ]
    
    def __init__(self):
        """Initialize the ethics tracker"""
        self.tracked_considerations: List[EthicalConsideration] = []
        self.irb_approvals: List[IRBApproval] = []
        self.safeguards: List[EthicalSafeguard] = []
    
    def extract_ethical_considerations(
        self,
        content: str,
        title: str = ""
    ) -> Dict[str, Any]:
        """
        Extract all ethical considerations from content.
        
        Args:
            content: Text content to analyze
            title: Optional paper title
        
        Returns:
            Dictionary with ethical information
        
        Requirements:
            - 10.1: Identify ethical considerations
            - 10.2: Document IRB approval
            - 10.3: Highlight ethical safeguards
            - 10.4: Identify ethical concerns
        """
        content_lower = content.lower()
        combined_text = f"{title} {content}".lower()
        
        # Identify research subject type
        subject_type = self._identify_subject_type(combined_text)
        
        # Extract IRB approval information
        irb_approval = self._extract_irb_approval(content)
        if irb_approval.has_approval:
            self.irb_approvals.append(irb_approval)
        
        # Extract ethical considerations by category
        considerations = []
        
        # Informed consent
        consent_considerations = self._extract_informed_consent(content)
        considerations.extend(consent_considerations)
        
        # Privacy and confidentiality
        privacy_considerations = self._extract_privacy_considerations(content)
        considerations.extend(privacy_considerations)
        
        # Vulnerable populations
        vulnerable_considerations = self._extract_vulnerable_population_considerations(content)
        considerations.extend(vulnerable_considerations)
        
        # Potential harms
        harm_considerations = self._extract_harm_considerations(content)
        considerations.extend(harm_considerations)
        
        # Animal welfare (if applicable)
        if subject_type == ResearchSubjectType.ANIMAL_SUBJECTS:
            animal_considerations = self._extract_animal_welfare_considerations(content)
            considerations.extend(animal_considerations)
        
        # Data security
        security_considerations = self._extract_data_security_considerations(content)
        considerations.extend(security_considerations)
        
        # Extract ethical safeguards
        safeguards = self._extract_safeguards(content)
        self.safeguards.extend(safeguards)
        
        # Track all considerations
        self.tracked_considerations.extend(considerations)
        
        return {
            "subject_type": subject_type.value,
            "irb_approval": irb_approval.to_dict(),
            "considerations": [c.to_dict() for c in considerations],
            "safeguards": [s.to_dict() for s in safeguards],
            "has_ethical_oversight": irb_approval.has_approval,
            "total_considerations": len(considerations),
            "total_safeguards": len(safeguards),
        }
    
    def _identify_subject_type(self, text: str) -> ResearchSubjectType:
        """
        Identify the type of research subjects.
        
        Args:
            text: Text to analyze
        
        Returns:
            ResearchSubjectType enum value
        """
        # Check for human subjects
        human_keywords = [
            'participants', 'subjects', 'respondents', 'patients',
            'volunteers', 'human', 'individuals', 'people'
        ]
        
        # Check for animal subjects
        animal_keywords = [
            'animal', 'mice', 'rats', 'primates', 'rodents',
            'specimens', 'iacuc'
        ]
        
        # Check for sensitive data
        data_keywords = [
            'personal data', 'sensitive data', 'health records',
            'medical records', 'patient data', 'confidential data'
        ]
        
        has_human = any(keyword in text for keyword in human_keywords)
        has_animal = any(keyword in text for keyword in animal_keywords)
        has_sensitive_data = any(keyword in text for keyword in data_keywords)
        
        if has_human:
            return ResearchSubjectType.HUMAN_SUBJECTS
        elif has_animal:
            return ResearchSubjectType.ANIMAL_SUBJECTS
        elif has_sensitive_data:
            return ResearchSubjectType.SENSITIVE_DATA
        else:
            return ResearchSubjectType.NONE
    
    def _extract_irb_approval(self, content: str) -> IRBApproval:
        """
        Extract IRB approval information.
        
        Args:
            content: Content to analyze
        
        Returns:
            IRBApproval object
        
        Requirements:
            - 10.2: Document IRB approval processes
        """
        content_lower = content.lower()
        
        # Check for IRB mentions
        has_irb_mention = any(
            re.search(pattern, content_lower, re.IGNORECASE)
            for pattern in self.IRB_PATTERNS
        )
        
        if not has_irb_mention:
            return IRBApproval(has_approval=False, confidence=0.9)
        
        # Extract IRB number
        irb_number = ""
        number_patterns = [
            r'irb\s*#?\s*(\d+[-/]?\d*)',
            r'protocol\s*#?\s*(\d+[-/]?\d*)',
            r'approval\s*number\s*[:#]?\s*(\d+[-/]?\d*)',
        ]
        
        for pattern in number_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                irb_number = match.group(1)
                break
        
        # Extract institution
        institution = ""
        institution_patterns = [
            r'(?:approved by|reviewed by)\s+(?:the\s+)?([A-Z][A-Za-z\s]+(?:University|College|Hospital|Institute))',
            r'([A-Z][A-Za-z\s]+(?:University|College|Hospital|Institute))\s+(?:IRB|ethics committee)',
        ]
        
        for pattern in institution_patterns:
            match = re.search(pattern, content)
            if match:
                institution = match.group(1).strip()
                break
        
        # Determine approval type
        approval_type = ""
        if 'exempt' in content_lower:
            approval_type = "exempt"
        elif 'expedited' in content_lower:
            approval_type = "expedited"
        elif 'full review' in content_lower or 'full board' in content_lower:
            approval_type = "full_review"
        
        # Extract details
        details = self._extract_irb_details(content)
        
        # Calculate confidence
        confidence = 0.5
        if irb_number:
            confidence += 0.3
        if institution:
            confidence += 0.2
        
        return IRBApproval(
            has_approval=True,
            irb_number=irb_number,
            institution=institution,
            approval_type=approval_type,
            details=details,
            confidence=min(confidence, 1.0),
        )
    
    def _extract_irb_details(self, content: str) -> str:
        """Extract details about IRB approval"""
        sentences = re.split(r'[.!?]+', content)
        irb_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(pattern in sentence_lower for pattern in ['irb', 'ethics committee', 'ethics approval']):
                irb_sentences.append(sentence.strip())
                if len(irb_sentences) >= 2:
                    break
        
        return '. '.join(irb_sentences) + '.' if irb_sentences else ""
    
    def _extract_informed_consent(self, content: str) -> List[EthicalConsideration]:
        """
        Extract informed consent considerations.
        
        Args:
            content: Content to analyze
        
        Returns:
            List of EthicalConsideration objects
        
        Requirements:
            - 10.1: Identify informed consent considerations
        """
        considerations = []
        content_lower = content.lower()
        
        # Check for informed consent mentions
        has_consent = any(
            re.search(pattern, content_lower, re.IGNORECASE)
            for pattern in self.INFORMED_CONSENT_PATTERNS
        )
        
        if not has_consent:
            return considerations
        
        # Extract consent-related sentences
        sentences = re.split(r'[.!?]+', content)
        consent_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(re.search(pattern, sentence_lower, re.IGNORECASE) 
                   for pattern in self.INFORMED_CONSENT_PATTERNS):
                consent_sentences.append(sentence.strip())
        
        # Create consideration
        if consent_sentences:
            description = "Informed consent procedures implemented"
            source_text = '. '.join(consent_sentences[:2]) + '.'
            
            # Check if properly addressed
            addressed = any(term in content_lower for term in [
                'obtained consent', 'signed consent', 'consent was obtained',
                'participants consented', 'consent form'
            ])
            
            mitigation = source_text if addressed else ""
            
            consideration = EthicalConsideration(
                category=EthicsCategory.INFORMED_CONSENT,
                description=description,
                severity="high" if not addressed else "low",
                addressed=addressed,
                mitigation=mitigation,
                source_text=source_text,
                confidence=0.8,
            )
            considerations.append(consideration)
        
        return considerations
    
    def _extract_privacy_considerations(self, content: str) -> List[EthicalConsideration]:
        """Extract privacy and confidentiality considerations"""
        considerations = []
        content_lower = content.lower()
        
        has_privacy = any(
            re.search(pattern, content_lower, re.IGNORECASE)
            for pattern in self.PRIVACY_PATTERNS
        )
        
        if not has_privacy:
            return considerations
        
        sentences = re.split(r'[.!?]+', content)
        privacy_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(re.search(pattern, sentence_lower, re.IGNORECASE) 
                   for pattern in self.PRIVACY_PATTERNS):
                privacy_sentences.append(sentence.strip())
        
        if privacy_sentences:
            description = "Privacy and confidentiality protections"
            source_text = '. '.join(privacy_sentences[:2]) + '.'
            
            addressed = any(term in content_lower for term in [
                'anonymized', 'de-identified', 'confidential', 'encrypted',
                'secure', 'protected'
            ])
            
            consideration = EthicalConsideration(
                category=EthicsCategory.PRIVACY_PROTECTION,
                description=description,
                severity="high" if not addressed else "low",
                addressed=addressed,
                mitigation=source_text if addressed else "",
                source_text=source_text,
                confidence=0.8,
            )
            considerations.append(consideration)
        
        return considerations
    
    def _extract_vulnerable_population_considerations(self, content: str) -> List[EthicalConsideration]:
        """Extract vulnerable population considerations"""
        considerations = []
        content_lower = content.lower()
        
        # Check for vulnerable population mentions
        vulnerable_types = []
        for pattern in self.VULNERABLE_POPULATION_PATTERNS:
            if re.search(pattern, content_lower, re.IGNORECASE):
                # Extract the type
                match = re.search(pattern, content_lower, re.IGNORECASE)
                if match:
                    vulnerable_types.append(match.group(0))
        
        if not vulnerable_types:
            return considerations
        
        # Extract relevant sentences
        sentences = re.split(r'[.!?]+', content)
        vulnerable_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(vtype in sentence_lower for vtype in vulnerable_types):
                vulnerable_sentences.append(sentence.strip())
        
        if vulnerable_sentences:
            description = f"Research involves vulnerable populations: {', '.join(set(vulnerable_types))}"
            source_text = '. '.join(vulnerable_sentences[:2]) + '.'
            
            # Check for special protections
            addressed = any(term in content_lower for term in [
                'special protection', 'additional safeguard', 'parental consent',
                'guardian consent', 'assent', 'extra precaution'
            ])
            
            consideration = EthicalConsideration(
                category=EthicsCategory.VULNERABLE_POPULATIONS,
                description=description,
                severity="high",
                addressed=addressed,
                mitigation=source_text if addressed else "",
                source_text=source_text,
                confidence=0.9,
            )
            considerations.append(consideration)
        
        return considerations
    
    def _extract_harm_considerations(self, content: str) -> List[EthicalConsideration]:
        """Extract potential harm considerations"""
        considerations = []
        content_lower = content.lower()
        
        has_harm = any(
            re.search(pattern, content_lower, re.IGNORECASE)
            for pattern in self.HARM_PATTERNS
        )
        
        if not has_harm:
            return considerations
        
        sentences = re.split(r'[.!?]+', content)
        harm_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(re.search(pattern, sentence_lower, re.IGNORECASE) 
                   for pattern in self.HARM_PATTERNS):
                harm_sentences.append(sentence.strip())
        
        if harm_sentences:
            description = "Potential harms and risks identified"
            source_text = '. '.join(harm_sentences[:2]) + '.'
            
            # Check for mitigation
            addressed = any(term in content_lower for term in [
                'mitigated', 'minimized', 'reduced', 'addressed',
                'safeguard', 'protection', 'prevented'
            ])
            
            # Determine severity
            severity = "high"
            if any(term in content_lower for term in ['minimal risk', 'low risk', 'negligible']):
                severity = "low"
            elif any(term in content_lower for term in ['moderate risk']):
                severity = "moderate"
            
            consideration = EthicalConsideration(
                category=EthicsCategory.POTENTIAL_HARMS,
                description=description,
                severity=severity,
                addressed=addressed,
                mitigation=source_text if addressed else "",
                source_text=source_text,
                confidence=0.7,
            )
            considerations.append(consideration)
        
        return considerations
    
    def _extract_animal_welfare_considerations(self, content: str) -> List[EthicalConsideration]:
        """Extract animal welfare considerations"""
        considerations = []
        content_lower = content.lower()
        
        has_animal = any(
            re.search(pattern, content_lower, re.IGNORECASE)
            for pattern in self.ANIMAL_PATTERNS
        )
        
        if not has_animal:
            return considerations
        
        sentences = re.split(r'[.!?]+', content)
        animal_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(re.search(pattern, sentence_lower, re.IGNORECASE) 
                   for pattern in self.ANIMAL_PATTERNS):
                animal_sentences.append(sentence.strip())
        
        if animal_sentences:
            description = "Animal welfare considerations"
            source_text = '. '.join(animal_sentences[:2]) + '.'
            
            # Check for IACUC approval
            addressed = any(term in content_lower for term in [
                'iacuc', 'animal care', 'humane', 'welfare',
                'approved', 'ethical treatment'
            ])
            
            consideration = EthicalConsideration(
                category=EthicsCategory.ANIMAL_WELFARE,
                description=description,
                severity="high" if not addressed else "moderate",
                addressed=addressed,
                mitigation=source_text if addressed else "",
                source_text=source_text,
                confidence=0.8,
            )
            considerations.append(consideration)
        
        return considerations
    
    def _extract_data_security_considerations(self, content: str) -> List[EthicalConsideration]:
        """Extract data security considerations"""
        considerations = []
        content_lower = content.lower()
        
        has_security = any(
            re.search(pattern, content_lower, re.IGNORECASE)
            for pattern in self.DATA_SECURITY_PATTERNS
        )
        
        if not has_security:
            return considerations
        
        sentences = re.split(r'[.!?]+', content)
        security_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(re.search(pattern, sentence_lower, re.IGNORECASE) 
                   for pattern in self.DATA_SECURITY_PATTERNS):
                security_sentences.append(sentence.strip())
        
        if security_sentences:
            description = "Data security measures"
            source_text = '. '.join(security_sentences[:2]) + '.'
            
            addressed = any(term in content_lower for term in [
                'encrypted', 'secure', 'protected', 'access control',
                'password', 'firewall'
            ])
            
            consideration = EthicalConsideration(
                category=EthicsCategory.DATA_SECURITY,
                description=description,
                severity="high" if not addressed else "low",
                addressed=addressed,
                mitigation=source_text if addressed else "",
                source_text=source_text,
                confidence=0.7,
            )
            considerations.append(consideration)
        
        return considerations
    
    def _extract_safeguards(self, content: str) -> List[EthicalSafeguard]:
        """
        Extract ethical safeguards implemented in the research.
        
        Args:
            content: Content to analyze
        
        Returns:
            List of EthicalSafeguard objects
        
        Requirements:
            - 10.3: Highlight ethical safeguards
        """
        safeguards = []
        content_lower = content.lower()
        
        # Define safeguard patterns and their categories
        safeguard_patterns = {
            'anonymization': (EthicsCategory.PRIVACY_PROTECTION, [
                r'anonymized', r'anonymization', r'anonymous'
            ]),
            'de-identification': (EthicsCategory.PRIVACY_PROTECTION, [
                r'de-identified', r'de-identification', r'deidentified'
            ]),
            'encryption': (EthicsCategory.DATA_SECURITY, [
                r'encrypted', r'encryption'
            ]),
            'informed_consent': (EthicsCategory.INFORMED_CONSENT, [
                r'informed consent', r'consent form', r'written consent'
            ]),
            'confidentiality_agreement': (EthicsCategory.CONFIDENTIALITY, [
                r'confidentiality agreement', r'non-disclosure'
            ]),
            'secure_storage': (EthicsCategory.DATA_SECURITY, [
                r'secure storage', r'secure server', r'locked cabinet'
            ]),
            'access_control': (EthicsCategory.DATA_SECURITY, [
                r'access control', r'restricted access', r'password protected'
            ]),
            'monitoring': (EthicsCategory.POTENTIAL_HARMS, [
                r'monitoring', r'oversight', r'supervision'
            ]),
        }
        
        # Extract safeguards
        for safeguard_type, (category, patterns) in safeguard_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content_lower, re.IGNORECASE):
                    # Find the sentence containing this safeguard
                    sentences = re.split(r'[.!?]+', content)
                    for sentence in sentences:
                        if re.search(pattern, sentence, re.IGNORECASE):
                            safeguard = EthicalSafeguard(
                                safeguard_type=safeguard_type.replace('_', ' ').title(),
                                description=sentence.strip(),
                                category=category,
                                effectiveness="implemented",
                                confidence=0.8,
                            )
                            safeguards.append(safeguard)
                            break
                    break
        
        return safeguards
    
    def generate_ethics_section(self) -> str:
        """
        Generate an ethics section for a report based on tracked considerations.
        
        Returns:
            Formatted ethics section text
        
        Requirements:
            - 10.5: Generate ethics section in reports
        """
        if not self.tracked_considerations and not self.irb_approvals:
            return ""
        
        sections = []
        
        # Header
        sections.append("## Ethical Considerations\n")
        
        # IRB Approval section
        if self.irb_approvals:
            sections.append("### Ethical Oversight\n")
            for irb in self.irb_approvals:
                if irb.has_approval:
                    text = "The research received ethical approval"
                    if irb.institution:
                        text += f" from {irb.institution}"
                    if irb.irb_number:
                        text += f" (Protocol: {irb.irb_number})"
                    if irb.approval_type:
                        text += f" through {irb.approval_type} review"
                    text += "."
                    sections.append(text + "\n")
                    
                    if irb.details:
                        sections.append(f"{irb.details}\n")
        
        # Group considerations by category
        by_category: Dict[EthicsCategory, List[EthicalConsideration]] = {}
        for consideration in self.tracked_considerations:
            if consideration.category not in by_category:
                by_category[consideration.category] = []
            by_category[consideration.category].append(consideration)
        
        # Write considerations by category
        if by_category:
            sections.append("\n### Ethical Considerations Identified\n")
            
            for category, considerations in sorted(by_category.items(), key=lambda x: x[0].value):
                category_name = category.value.replace('_', ' ').title()
                sections.append(f"\n**{category_name}:**\n")
                
                for consideration in considerations:
                    sections.append(f"- {consideration.description}")
                    if consideration.addressed and consideration.mitigation:
                        sections.append(f" (Addressed: {consideration.mitigation[:100]}...)")
                    elif not consideration.addressed:
                        sections.append(f" (Severity: {consideration.severity})")
                    sections.append("\n")
        
        # Safeguards section
        if self.safeguards:
            sections.append("\n### Ethical Safeguards Implemented\n")
            
            # Group safeguards by category
            safeguards_by_category: Dict[EthicsCategory, List[EthicalSafeguard]] = {}
            for safeguard in self.safeguards:
                if safeguard.category not in safeguards_by_category:
                    safeguards_by_category[safeguard.category] = []
                safeguards_by_category[safeguard.category].append(safeguard)
            
            for category, safeguards in sorted(safeguards_by_category.items(), key=lambda x: x[0].value):
                for safeguard in safeguards:
                    sections.append(f"- **{safeguard.safeguard_type}**: {safeguard.description[:150]}\n")
        
        # Summary
        sections.append("\n### Summary\n")
        total_considerations = len(self.tracked_considerations)
        addressed_count = sum(1 for c in self.tracked_considerations if c.addressed)
        
        if total_considerations > 0:
            sections.append(
                f"A total of {total_considerations} ethical considerations were identified, "
                f"of which {addressed_count} ({addressed_count/total_considerations*100:.0f}%) "
                f"were explicitly addressed in the research. "
            )
        
        if self.safeguards:
            sections.append(
                f"{len(self.safeguards)} ethical safeguards were implemented to protect "
                f"participants and ensure research integrity."
            )
        
        return '\n'.join(sections)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about tracked ethical considerations.
        
        Returns:
            Dictionary with statistics
        """
        if not self.tracked_considerations:
            return {
                "total_considerations": 0,
                "addressed_count": 0,
                "addressed_percentage": 0.0,
                "by_category": {},
                "by_severity": {},
                "has_irb_approval": False,
                "total_safeguards": 0,
            }
        
        total = len(self.tracked_considerations)
        addressed = sum(1 for c in self.tracked_considerations if c.addressed)
        
        # Count by category
        by_category = {}
        for consideration in self.tracked_considerations:
            cat = consideration.category.value
            by_category[cat] = by_category.get(cat, 0) + 1
        
        # Count by severity
        by_severity = {}
        for consideration in self.tracked_considerations:
            sev = consideration.severity
            by_severity[sev] = by_severity.get(sev, 0) + 1
        
        return {
            "total_considerations": total,
            "addressed_count": addressed,
            "addressed_percentage": (addressed / total) * 100 if total > 0 else 0.0,
            "by_category": by_category,
            "by_severity": by_severity,
            "has_irb_approval": len(self.irb_approvals) > 0 and any(irb.has_approval for irb in self.irb_approvals),
            "total_safeguards": len(self.safeguards),
        }
    
    def log_ethics_summary(self):
        """Log a summary of ethical considerations"""
        stats = self.get_statistics()
        
        logger.info("=" * 60)
        logger.info("ETHICAL CONSIDERATIONS SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Total considerations: {stats['total_considerations']}")
        logger.info(f"Addressed: {stats['addressed_count']} ({stats['addressed_percentage']:.1f}%)")
        logger.info(f"IRB approval: {'Yes' if stats['has_irb_approval'] else 'No'}")
        logger.info(f"Safeguards implemented: {stats['total_safeguards']}")
        
        if stats['by_category']:
            logger.info("\nBy category:")
            for category, count in sorted(stats['by_category'].items()):
                logger.info(f"  - {category}: {count}")
        
        if stats['by_severity']:
            logger.info("\nBy severity:")
            for severity, count in sorted(stats['by_severity'].items()):
                logger.info(f"  - {severity}: {count}")
        
        logger.info("=" * 60)


def extract_ethics_from_paper(
    content: str,
    title: str = ""
) -> Dict[str, Any]:
    """
    Convenience function to extract ethical considerations from a paper.
    
    Args:
        content: Paper content
        title: Paper title
    
    Returns:
        Dictionary with ethical information
    
    Example:
        >>> content = "This study was approved by the IRB..."
        >>> result = extract_ethics_from_paper(content)
        >>> print(result['irb_approval']['has_approval'])
        True
    """
    tracker = EthicsTracker()
    return tracker.extract_ethical_considerations(content, title)
