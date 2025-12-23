"""
CryptoTracker - Advanced Blockchain Forensics & Victim Support System
Main Flask Application
"""
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from datetime import datetime
import json

from config import config
from src.blockchain import BlockchainAnalyzer
from src.osint import OSINTCollector
from src.recovery import RecoveryAssistant
from src.utils import (
    validate_ethereum_address, 
    validate_transaction_hash,
    sanitize_input,
    export_to_json,
    generate_report_filename
)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config['development'])
CORS(app)

# Initialize components
blockchain_analyzer = None
osint_collector = None
recovery_assistant = RecoveryAssistant()

def get_blockchain_analyzer():
    """Get or create blockchain analyzer instance"""
    global blockchain_analyzer
    if blockchain_analyzer is None:
        api_key = os.getenv('ETHERSCAN_API_KEY', '')
        blockchain_analyzer = BlockchainAnalyzer(api_key=api_key)
    return blockchain_analyzer

def get_osint_collector():
    """Get or create OSINT collector instance"""
    global osint_collector
    if osint_collector is None:
        api_key = os.getenv('ETHERSCAN_API_KEY', '')
        osint_collector = OSINTCollector(etherscan_api_key=api_key)
    return osint_collector

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_address():
    """
    Analyze a cryptocurrency address
    """
    try:
        data = request.get_json()
        address = sanitize_input(data.get('address', ''))
        
        if not validate_ethereum_address(address):
            return jsonify({
                'success': False,
                'error': 'Invalid Ethereum address format'
            }), 400
        
        analyzer = get_blockchain_analyzer()
        
        # Perform comprehensive analysis
        result = {
            'success': True,
            'address': address,
            'timestamp': datetime.now().isoformat(),
            'balance': analyzer.get_address_balance(address),
            'transaction_pattern': analyzer.analyze_transaction_pattern(address),
            'address_poisoning': analyzer.detect_address_poisoning(address),
            'mixer_detection': analyzer.detect_mixer_usage(address),
            'exchange_interaction': analyzer.detect_exchange_interaction(address)
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/trace', methods=['POST'])
def trace_funds():
    """
    Trace funds from an address
    """
    try:
        data = request.get_json()
        address = sanitize_input(data.get('address', ''))
        max_depth = int(data.get('max_depth', 5))
        
        if not validate_ethereum_address(address):
            return jsonify({
                'success': False,
                'error': 'Invalid Ethereum address format'
            }), 400
        
        analyzer = get_blockchain_analyzer()
        trace_result = analyzer.trace_funds(address, max_depth=max_depth)
        
        return jsonify({
            'success': True,
            'trace': trace_result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/transaction', methods=['POST'])
def analyze_transaction():
    """
    Analyze a specific transaction
    """
    try:
        data = request.get_json()
        tx_hash = sanitize_input(data.get('tx_hash', ''))
        
        if not validate_transaction_hash(tx_hash):
            return jsonify({
                'success': False,
                'error': 'Invalid transaction hash format'
            }), 400
        
        analyzer = get_blockchain_analyzer()
        tx_details = analyzer.get_transaction_details(tx_hash)
        
        if not tx_details:
            return jsonify({
                'success': False,
                'error': 'Transaction not found'
            }), 404
        
        # Analyze both sender and receiver
        from_analysis = analyzer.analyze_transaction_pattern(tx_details['from'])
        to_analysis = analyzer.analyze_transaction_pattern(tx_details['to'])
        
        return jsonify({
            'success': True,
            'transaction': tx_details,
            'from_analysis': from_analysis,
            'to_analysis': to_analysis
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/osint', methods=['POST'])
def get_osint():
    """
    Get OSINT data for an address
    """
    try:
        data = request.get_json()
        address = sanitize_input(data.get('address', ''))
        
        if not validate_ethereum_address(address):
            return jsonify({
                'success': False,
                'error': 'Invalid Ethereum address format'
            }), 400
        
        collector = get_osint_collector()
        osint_data = collector.collect_all_osint(address)
        
        return jsonify({
            'success': True,
            'osint': osint_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/osint/report', methods=['POST'])
def generate_osint_report():
    """
    Generate comprehensive OSINT report
    """
    try:
        data = request.get_json()
        address = sanitize_input(data.get('address', ''))
        
        if not validate_ethereum_address(address):
            return jsonify({
                'success': False,
                'error': 'Invalid Ethereum address format'
            }), 400
        
        collector = get_osint_collector()
        report = collector.generate_osint_report(address)
        
        return jsonify({
            'success': True,
            'report': report
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recovery/plan', methods=['POST'])
def generate_recovery_plan():
    """
    Generate recovery plan for theft victim
    """
    try:
        data = request.get_json()
        incident_data = data.get('incident_data', {})
        
        plan = recovery_assistant.generate_recovery_plan(incident_data)
        
        return jsonify({
            'success': True,
            'plan': plan
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recovery/whitehat', methods=['POST'])
def generate_whitehat_message():
    """
    Generate whitehat negotiation message
    """
    try:
        data = request.get_json()
        incident_data = data.get('incident_data', {})
        bounty_percentage = int(data.get('bounty_percentage', 10))
        
        message = recovery_assistant.generate_whitehat_message(
            incident_data, 
            bounty_percentage
        )
        
        return jsonify({
            'success': True,
            'message': message
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recovery/law-enforcement', methods=['POST'])
def generate_le_package():
    """
    Generate law enforcement evidence package
    """
    try:
        data = request.get_json()
        incident_data = data.get('incident_data', {})
        
        # Get blockchain analysis
        analyzer = get_blockchain_analyzer()
        attacker_address = incident_data.get('attacker_address', '')
        
        if validate_ethereum_address(attacker_address):
            blockchain_analysis = {
                'pattern': analyzer.analyze_transaction_pattern(attacker_address),
                'mixer': analyzer.detect_mixer_usage(attacker_address),
                'exchange': analyzer.detect_exchange_interaction(attacker_address)
            }
        else:
            blockchain_analysis = {}
        
        # Get OSINT data
        collector = get_osint_collector()
        if validate_ethereum_address(attacker_address):
            osint_data = collector.collect_all_osint(attacker_address)
        else:
            osint_data = {}
        
        # Generate package
        package = recovery_assistant.generate_law_enforcement_package(
            incident_data,
            blockchain_analysis,
            osint_data
        )
        
        return jsonify({
            'success': True,
            'package': package
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/recovery/exchange-report', methods=['POST'])
def generate_exchange_report():
    """
    Generate exchange report template
    """
    try:
        data = request.get_json()
        incident_data = data.get('incident_data', {})
        exchange_name = data.get('exchange_name', 'Exchange')
        
        report = recovery_assistant.generate_exchange_report_template(
            incident_data,
            exchange_name
        )
        
        return jsonify({
            'success': True,
            'report': report
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/prevention', methods=['GET'])
def get_prevention_tips():
    """
    Get prevention recommendations
    """
    try:
        recommendations = recovery_assistant.get_prevention_recommendations()
        
        return jsonify({
            'success': True,
            'recommendations': recommendations
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/export', methods=['POST'])
def export_report():
    """
    Export analysis report as JSON
    """
    try:
        data = request.get_json()
        report_data = data.get('report_data', {})
        
        filename = generate_report_filename('cryptotracker_report')
        filepath = os.path.join('data', filename)
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        
        if export_to_json(report_data, filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype='application/json'
            )
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to export report'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Ensure required directories exist
    os.makedirs('data', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Run the application
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)