"""
Recovery Assistance System
Helps victims of crypto theft with recovery strategies and evidence collection
"""
from typing import Dict, List, Optional
from datetime import datetime
import json

class RecoveryAssistant:
    """
    Provides recovery assistance for crypto theft victims
    """
    
    def __init__(self):
        self.recovery_strategies = []
        
    def generate_recovery_plan(self, incident_data: Dict) -> Dict:
        """
        Generate a comprehensive recovery plan based on incident details
        """
        plan = {
            'incident_id': self._generate_incident_id(),
            'timestamp': datetime.now().isoformat(),
            'incident_summary': incident_data,
            'immediate_actions': self._get_immediate_actions(incident_data),
            'short_term_actions': self._get_short_term_actions(incident_data),
            'long_term_actions': self._get_long_term_actions(incident_data),
            'recovery_probability': self._estimate_recovery_probability(incident_data),
            'estimated_timeline': self._estimate_timeline(incident_data)
        }
        
        return plan
    
    def _generate_incident_id(self) -> str:
        """Generate unique incident ID"""
        return f"INC-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _get_immediate_actions(self, incident_data: Dict) -> List[Dict]:
        """
        Get immediate actions to take (within first hour)
        """
        actions = []
        
        # Action 1: Freeze stablecoins if possible
        if self._involves_freezable_token(incident_data):
            actions.append({
                'priority': 'CRITICAL',
                'action': 'Contact Token Issuer',
                'description': 'If stolen funds include USDT or USDC, contact Tether/Circle immediately to request freeze',
                'contacts': [
                    'Tether: https://tether.to/en/contact-us/',
                    'Circle: https://www.circle.com/en/legal/law-enforcement'
                ],
                'deadline': 'Within 1 hour',
                'status': 'PENDING'
            })
        
        # Action 2: Document everything
        actions.append({
            'priority': 'CRITICAL',
            'action': 'Document All Evidence',
            'description': 'Take screenshots of wallet, transactions, and any communications',
            'steps': [
                'Screenshot your wallet showing the transaction',
                'Save transaction hashes',
                'Record exact time of theft',
                'Save any phishing emails/messages',
                'Document your actions leading to the theft'
            ],
            'deadline': 'Immediately',
            'status': 'PENDING'
        })
        
        # Action 3: Report to exchanges
        if self._funds_went_to_exchange(incident_data):
            actions.append({
                'priority': 'CRITICAL',
                'action': 'Alert Exchanges',
                'description': 'Contact exchanges where funds may have been sent',
                'steps': [
                    'Identify which exchange received funds',
                    'Contact their fraud/security team',
                    'Provide transaction hash and details',
                    'Request account freeze'
                ],
                'deadline': 'Within 2 hours',
                'status': 'PENDING'
            })
        
        # Action 4: Change security credentials
        actions.append({
            'priority': 'HIGH',
            'action': 'Secure Your Accounts',
            'description': 'Change passwords and enable 2FA on all crypto accounts',
            'steps': [
                'Change wallet passwords',
                'Enable 2FA on all exchanges',
                'Check for malware on your device',
                'Review recent account activity',
                'Revoke any suspicious token approvals'
            ],
            'deadline': 'Within 4 hours',
            'status': 'PENDING'
        })
        
        return actions
    
    def _get_short_term_actions(self, incident_data: Dict) -> List[Dict]:
        """
        Get short-term actions (within first 24-48 hours)
        """
        actions = []
        
        # Action 1: File police report
        actions.append({
            'priority': 'HIGH',
            'action': 'File Police Report',
            'description': 'File official report with local law enforcement',
            'steps': [
                'Visit local police station',
                'Bring all documentation and evidence',
                'Get case number for reference',
                'Request copy of police report'
            ],
            'deadline': 'Within 24 hours',
            'status': 'PENDING'
        })
        
        # Action 2: Report to FBI IC3
        actions.append({
            'priority': 'HIGH',
            'action': 'Report to FBI IC3',
            'description': 'File complaint with FBI Internet Crime Complaint Center',
            'website': 'https://www.ic3.gov',
            'steps': [
                'Visit IC3 website',
                'Complete online complaint form',
                'Include all transaction details',
                'Save complaint number'
            ],
            'deadline': 'Within 24 hours',
            'status': 'PENDING'
        })
        
        # Action 3: Attempt whitehat negotiation
        actions.append({
            'priority': 'MEDIUM',
            'action': 'Whitehat Negotiation',
            'description': 'Send on-chain message offering bounty for return of funds',
            'steps': [
                'Prepare professional message',
                'Offer 10% bounty for 90% return',
                'Mention law enforcement involvement',
                'Set deadline for response',
                'Use secure communication channel'
            ],
            'deadline': 'Within 48 hours',
            'status': 'PENDING'
        })
        
        # Action 4: Engage recovery service
        actions.append({
            'priority': 'MEDIUM',
            'action': 'Contact Recovery Services',
            'description': 'Engage professional blockchain forensics firms',
            'recommended_services': [
                'Chainalysis - Enterprise blockchain analysis',
                'TRM Labs - Crypto compliance and investigations',
                'CipherBlade - Crypto investigation specialists',
                'Elliptic - Blockchain analytics'
            ],
            'deadline': 'Within 48 hours',
            'status': 'PENDING'
        })
        
        return actions
    
    def _get_long_term_actions(self, incident_data: Dict) -> List[Dict]:
        """
        Get long-term actions (weeks to months)
        """
        actions = []
        
        # Action 1: Monitor blockchain
        actions.append({
            'priority': 'MEDIUM',
            'action': 'Continuous Monitoring',
            'description': 'Monitor stolen funds for movement',
            'steps': [
                'Set up alerts for address activity',
                'Track funds through mixers',
                'Watch for exchange deposits',
                'Document all movements'
            ],
            'timeline': 'Ongoing',
            'status': 'PENDING'
        })
        
        # Action 2: Legal action
        actions.append({
            'priority': 'MEDIUM',
            'action': 'Consult Legal Counsel',
            'description': 'Explore legal options for recovery',
            'steps': [
                'Consult with crypto-specialized attorney',
                'Explore civil lawsuit options',
                'Consider international legal cooperation',
                'Evaluate cost vs. potential recovery'
            ],
            'timeline': '1-3 months',
            'status': 'PENDING'
        })
        
        # Action 3: Community awareness
        actions.append({
            'priority': 'LOW',
            'action': 'Warn Community',
            'description': 'Share your experience to prevent others from falling victim',
            'steps': [
                'Post on crypto forums (Reddit, Twitter)',
                'Report to scam databases',
                'Share attacker addresses',
                'Document attack method'
            ],
            'timeline': 'Ongoing',
            'status': 'PENDING'
        })
        
        return actions
    
    def _involves_freezable_token(self, incident_data: Dict) -> bool:
        """Check if incident involves freezable tokens like USDT/USDC"""
        token_type = incident_data.get('token_type', '').upper()
        return token_type in ['USDT', 'USDC', 'BUSD']
    
    def _funds_went_to_exchange(self, incident_data: Dict) -> bool:
        """Check if funds were sent to a known exchange"""
        return incident_data.get('exchange_detected', False)
    
    def _estimate_recovery_probability(self, incident_data: Dict) -> Dict:
        """
        Estimate probability of fund recovery
        """
        probability_score = 0
        factors = []
        
        # Factor 1: Time elapsed
        time_elapsed = incident_data.get('time_elapsed_hours', 0)
        if time_elapsed < 1:
            probability_score += 30
            factors.append('Quick response time increases chances')
        elif time_elapsed < 24:
            probability_score += 20
            factors.append('Response within 24 hours is positive')
        else:
            probability_score += 5
            factors.append('Delayed response reduces chances')
        
        # Factor 2: Funds went to exchange
        if self._funds_went_to_exchange(incident_data):
            probability_score += 40
            factors.append('Funds at exchange - high recovery potential')
        
        # Factor 3: Freezable tokens
        if self._involves_freezable_token(incident_data):
            probability_score += 20
            factors.append('Freezable stablecoin - can be frozen by issuer')
        
        # Factor 4: Mixer usage
        if incident_data.get('mixer_detected', False):
            probability_score -= 30
            factors.append('Mixer usage significantly reduces recovery chances')
        
        # Factor 5: Amount stolen
        amount = incident_data.get('amount_usd', 0)
        if amount > 100000:
            probability_score += 10
            factors.append('Large amount - more resources for recovery')
        
        # Normalize score
        probability_score = max(0, min(100, probability_score))
        
        # Determine category
        if probability_score >= 70:
            category = 'HIGH'
            description = 'Good chance of recovery with proper actions'
        elif probability_score >= 40:
            category = 'MEDIUM'
            description = 'Moderate chance of recovery, pursue all options'
        elif probability_score >= 20:
            category = 'LOW'
            description = 'Difficult but not impossible, continue efforts'
        else:
            category = 'VERY LOW'
            description = 'Recovery unlikely but document for law enforcement'
        
        return {
            'probability_score': probability_score,
            'category': category,
            'description': description,
            'factors': factors
        }
    
    def _estimate_timeline(self, incident_data: Dict) -> Dict:
        """
        Estimate timeline for recovery efforts
        """
        if self._funds_went_to_exchange(incident_data):
            return {
                'best_case': '1-2 weeks',
                'typical_case': '1-3 months',
                'worst_case': '6+ months',
                'note': 'Exchange cooperation can expedite recovery'
            }
        elif incident_data.get('mixer_detected', False):
            return {
                'best_case': '3-6 months',
                'typical_case': '6-12 months',
                'worst_case': 'May not recover',
                'note': 'Mixer usage significantly complicates recovery'
            }
        else:
            return {
                'best_case': '2-4 weeks',
                'typical_case': '2-6 months',
                'worst_case': '12+ months',
                'note': 'Timeline depends on attacker cooperation and law enforcement'
            }
    
    def generate_whitehat_message(self, incident_data: Dict, bounty_percentage: int = 10) -> str:
        """
        Generate professional whitehat negotiation message
        """
        amount = incident_data.get('amount_usd', 0)
        bounty_amount = amount * (bounty_percentage / 100)
        return_percentage = 100 - bounty_percentage
        
        message = f"""
TO THE ADDRESS HOLDING OUR FUNDS:

We are reaching out regarding the {amount:,.2f} USD transferred to your address.

WHITEHAT BOUNTY OFFER:
- Return {return_percentage}% of funds ({amount * (return_percentage/100):,.2f} USD)
- Keep {bounty_percentage}% as whitehat bounty ({bounty_amount:,.2f} USD)
- No questions asked, no legal action

CURRENT SITUATION:
- Law enforcement has been notified (Case filed)
- Multiple exchanges are monitoring these funds
- Blockchain forensics firms are tracking movements
- Every transaction is being documented

YOUR OPTIONS:
1. Accept this offer and return funds (RECOMMENDED)
2. Continue holding - face legal consequences and exchange freezes

TIME LIMIT: 72 hours from this message

CONTACT:
- Reply via on-chain message to this address
- Or contact: [Secure email/contact method]

This is your best opportunity to resolve this situation favorably.

Timestamp: {datetime.now().isoformat()}
"""
        return message
    
    def generate_law_enforcement_package(self, incident_data: Dict, 
                                        blockchain_analysis: Dict,
                                        osint_data: Dict) -> Dict:
        """
        Generate comprehensive evidence package for law enforcement
        """
        package = {
            'package_id': self._generate_incident_id(),
            'generated': datetime.now().isoformat(),
            'victim_information': {
                'incident_date': incident_data.get('incident_date'),
                'amount_stolen': incident_data.get('amount_usd'),
                'token_type': incident_data.get('token_type'),
                'victim_address': incident_data.get('victim_address'),
                'attacker_address': incident_data.get('attacker_address')
            },
            'incident_timeline': self._build_incident_timeline(incident_data),
            'blockchain_evidence': blockchain_analysis,
            'osint_intelligence': osint_data,
            'recommended_actions': self._get_le_recommended_actions(incident_data),
            'supporting_documents': []
        }
        
        return package
    
    def _build_incident_timeline(self, incident_data: Dict) -> List[Dict]:
        """
        Build detailed timeline of incident
        """
        timeline = []
        
        # Add known events
        if incident_data.get('test_transaction_time'):
            timeline.append({
                'timestamp': incident_data['test_transaction_time'],
                'event': 'Test transaction sent',
                'details': 'Victim sent small test amount'
            })
        
        if incident_data.get('theft_time'):
            timeline.append({
                'timestamp': incident_data['theft_time'],
                'event': 'Main theft transaction',
                'details': f"Large amount stolen: {incident_data.get('amount_usd')} USD"
            })
        
        if incident_data.get('conversion_time'):
            timeline.append({
                'timestamp': incident_data['conversion_time'],
                'event': 'Token conversion',
                'details': 'Attacker converted stolen tokens'
            })
        
        if incident_data.get('mixer_deposit_time'):
            timeline.append({
                'timestamp': incident_data['mixer_deposit_time'],
                'event': 'Mixer deposit',
                'details': 'Funds deposited into Tornado Cash or similar mixer'
            })
        
        return sorted(timeline, key=lambda x: x['timestamp'])
    
    def _get_le_recommended_actions(self, incident_data: Dict) -> List[str]:
        """
        Get recommended actions for law enforcement
        """
        actions = [
            'Issue preservation requests to identified exchanges',
            'Coordinate with blockchain forensics firms (Chainalysis, TRM Labs)',
            'Monitor known off-ramping points for stolen funds',
            'Issue subpoenas for exchange account information if funds deposited',
            'Coordinate with international law enforcement if cross-border'
        ]
        
        if incident_data.get('mixer_detected'):
            actions.append('Monitor mixer outputs for pattern matching')
            actions.append('Coordinate with other victims of similar attacks')
        
        return actions
    
    def generate_exchange_report_template(self, incident_data: Dict, 
                                         exchange_name: str) -> str:
        """
        Generate template for reporting to exchanges
        """
        template = f"""
URGENT: Stolen Cryptocurrency Report

To: {exchange_name} Security/Fraud Team

INCIDENT SUMMARY:
- Date of Theft: {incident_data.get('incident_date')}
- Amount Stolen: {incident_data.get('amount_usd')} USD
- Token Type: {incident_data.get('token_type')}
- Victim Address: {incident_data.get('victim_address')}
- Attacker Address: {incident_data.get('attacker_address')}

TRANSACTION DETAILS:
- Theft Transaction Hash: {incident_data.get('theft_tx_hash')}
- Deposit to Exchange (if applicable): {incident_data.get('exchange_deposit_tx')}

REQUEST:
We request immediate action to:
1. Freeze the account that received these funds
2. Preserve all account information for law enforcement
3. Prevent withdrawal of stolen funds
4. Provide account details to law enforcement

LAW ENFORCEMENT:
- Police Report Filed: {incident_data.get('police_report_number', 'Pending')}
- FBI IC3 Complaint: {incident_data.get('ic3_complaint_number', 'Pending')}

CONTACT INFORMATION:
- Name: [Your Name]
- Email: [Your Email]
- Phone: [Your Phone]

SUPPORTING EVIDENCE:
- Blockchain explorer links attached
- Transaction screenshots attached
- Police report attached (when available)

TIME SENSITIVITY:
This is a time-sensitive matter. The attacker may attempt to withdraw funds at any moment.

Thank you for your immediate attention to this matter.

Sincerely,
[Your Name]
[Date]
"""
        return template
    
    def get_prevention_recommendations(self) -> List[Dict]:
        """
        Get recommendations to prevent future attacks
        """
        return [
            {
                'category': 'Address Verification',
                'recommendations': [
                    'Always verify the FULL address, not just first/last characters',
                    'Use address book/contacts for frequent transfers',
                    'Bookmark legitimate addresses in your browser',
                    'Use ENS names instead of raw addresses when possible'
                ]
            },
            {
                'category': 'Transaction Safety',
                'recommendations': [
                    'Always send test transaction first',
                    'Wait and verify test transaction before sending large amounts',
                    'Use hardware wallet for large transactions',
                    'Enable transaction simulation (Tenderly, Pocket Universe)',
                    'Review transaction details on hardware wallet screen'
                ]
            },
            {
                'category': 'Security Practices',
                'recommendations': [
                    'Use hardware wallet for large holdings',
                    'Enable 2FA on all exchanges',
                    'Keep software and wallets updated',
                    'Be suspicious of urgent requests',
                    'Never share seed phrases or private keys'
                ]
            },
            {
                'category': 'Awareness',
                'recommendations': [
                    'Learn about common scam types',
                    'Be aware of address poisoning attacks',
                    'Verify URLs before connecting wallet',
                    'Be cautious of too-good-to-be-true offers',
                    'Join crypto security communities'
                ]
            }
        ]