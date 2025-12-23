// CryptoTracker - Main Application JavaScript

// API Base URL
const API_BASE = '/api';

// Utility Functions
function showLoading() {
    document.getElementById('loadingOverlay').classList.remove('hidden');
}

function hideLoading() {
    document.getElementById('loadingOverlay').classList.add('hidden');
}

function showError(message) {
    alert(`Error: ${message}`);
}

function formatAddress(address) {
    if (!address) return 'N/A';
    return `${address.substring(0, 10)}...${address.substring(address.length - 8)}`;
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatEth(amount) {
    return `${parseFloat(amount).toFixed(4)} ETH`;
}

function getRiskBadgeClass(riskLevel) {
    const level = riskLevel.toUpperCase();
    if (level === 'CRITICAL') return 'risk-critical';
    if (level === 'HIGH') return 'risk-high';
    if (level === 'MEDIUM') return 'risk-medium';
    return 'risk-low';
}

// Address Analysis
document.getElementById('analyzeBtn')?.addEventListener('click', async () => {
    const address = document.getElementById('addressInput').value.trim();
    
    if (!address) {
        showError('Please enter an address');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ address })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayAnalysisResults(data);
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to analyze address: ' + error.message);
    } finally {
        hideLoading();
    }
});

function displayAnalysisResults(data) {
    const resultsDiv = document.getElementById('analysisResults');
    resultsDiv.classList.remove('hidden');
    
    const balance = data.balance || {};
    const pattern = data.transaction_pattern || {};
    const poisoning = data.address_poisoning || {};
    const mixer = data.mixer_detection || {};
    const exchange = data.exchange_interaction || {};
    
    resultsDiv.innerHTML = `
        <div class="fade-in">
            <h3 class="mb-3">Analysis Results</h3>
            
            <!-- Balance -->
            <div class="result-item">
                <div class="result-label">Current Balance</div>
                <div class="result-value">${formatEth(balance.balance_eth || 0)}</div>
            </div>
            
            <!-- Risk Assessment -->
            <div class="result-item">
                <div class="result-label">Risk Level</div>
                <div class="result-value">
                    <span class="risk-badge ${getRiskBadgeClass(pattern.risk_level || 'LOW')}">
                        ${pattern.risk_level || 'LOW'}
                    </span>
                    <span style="margin-left: 1rem;">Score: ${pattern.risk_score || 0}/100</span>
                </div>
            </div>
            
            <!-- Transaction Stats -->
            <div class="result-item">
                <div class="result-label">Transaction Statistics</div>
                <div class="result-value">
                    <div>Total Transactions: ${pattern.total_transactions || 0}</div>
                    <div>Value Sent: ${formatEth(pattern.total_value_sent || 0)}</div>
                    <div>Value Received: ${formatEth(pattern.total_value_received || 0)}</div>
                </div>
            </div>
            
            <!-- Address Poisoning Detection -->
            ${poisoning.total_suspicious > 0 ? `
                <div class="result-item">
                    <div class="result-label">⚠️ Address Poisoning Detected</div>
                    <div class="result-value">
                        <div class="alert alert-warning">
                            Found ${poisoning.total_suspicious} suspicious address(es) with similar patterns.
                            This address may be involved in address poisoning attacks.
                        </div>
                    </div>
                </div>
            ` : ''}
            
            <!-- Mixer Detection -->
            ${mixer.mixer_detected ? `
                <div class="result-item">
                    <div class="result-label">🔴 Mixer Usage Detected</div>
                    <div class="result-value">
                        <div class="alert alert-danger">
                            This address has interacted with cryptocurrency mixers (${mixer.total_interactions} interaction(s)).
                            This significantly complicates fund tracking.
                        </div>
                    </div>
                </div>
            ` : ''}
            
            <!-- Exchange Detection -->
            ${exchange.exchange_detected ? `
                <div class="result-item">
                    <div class="result-label">✅ Exchange Interaction Detected</div>
                    <div class="result-value">
                        <div class="alert alert-success">
                            Funds have been sent to known exchanges (${exchange.total_interactions} interaction(s)).
                            Recovery potential: ${exchange.recovery_potential}
                        </div>
                        ${exchange.interactions.map(int => `
                            <div style="margin-top: 0.5rem;">
                                <strong>${int.exchange}</strong> - ${formatEth(int.value)}
                            </div>
                        `).join('')}
                    </div>
                </div>
            ` : ''}
            
            <!-- Risk Factors -->
            ${pattern.risk_factors && pattern.risk_factors.length > 0 ? `
                <div class="result-item">
                    <div class="result-label">Risk Factors</div>
                    <div class="result-value">
                        <ul style="list-style: none; padding: 0;">
                            ${pattern.risk_factors.map(factor => `
                                <li style="margin-bottom: 0.5rem;">⚠️ ${factor}</li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            ` : ''}
            
            <!-- Explorer Link -->
            <div class="result-item">
                <div class="result-label">View on Explorer</div>
                <div class="result-value">
                    <a href="https://etherscan.io/address/${data.address}" target="_blank" style="color: var(--primary-color);">
                        View on Etherscan →
                    </a>
                </div>
            </div>
        </div>
    `;
}

// Transaction Tracking
document.getElementById('trackTxBtn')?.addEventListener('click', async () => {
    const txHash = document.getElementById('txHashInput').value.trim();
    
    if (!txHash) {
        showError('Please enter a transaction hash');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/transaction`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ tx_hash: txHash })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayTransactionResults(data);
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to track transaction: ' + error.message);
    } finally {
        hideLoading();
    }
});

function displayTransactionResults(data) {
    const resultsDiv = document.getElementById('txResults');
    resultsDiv.classList.remove('hidden');
    
    const tx = data.transaction || {};
    const fromAnalysis = data.from_analysis || {};
    const toAnalysis = data.to_analysis || {};
    
    resultsDiv.innerHTML = `
        <div class="fade-in">
            <h3 class="mb-3">Transaction Details</h3>
            
            <div class="result-item">
                <div class="result-label">Transaction Hash</div>
                <div class="result-value" style="word-break: break-all;">${tx.hash}</div>
            </div>
            
            <div class="result-item">
                <div class="result-label">From</div>
                <div class="result-value">
                    ${formatAddress(tx.from)}
                    <span class="risk-badge ${getRiskBadgeClass(fromAnalysis.risk_level || 'LOW')}" style="margin-left: 1rem;">
                        ${fromAnalysis.risk_level || 'LOW'}
                    </span>
                </div>
            </div>
            
            <div class="result-item">
                <div class="result-label">To</div>
                <div class="result-value">
                    ${formatAddress(tx.to)}
                    <span class="risk-badge ${getRiskBadgeClass(toAnalysis.risk_level || 'LOW')}" style="margin-left: 1rem;">
                        ${toAnalysis.risk_level || 'LOW'}
                    </span>
                </div>
            </div>
            
            <div class="result-item">
                <div class="result-label">Value</div>
                <div class="result-value">${formatEth(tx.value || 0)}</div>
            </div>
            
            <div class="result-item">
                <div class="result-label">Status</div>
                <div class="result-value">
                    ${tx.status ? '<span class="text-success">✓ Success</span>' : '<span class="text-danger">✗ Failed</span>'}
                </div>
            </div>
            
            <div class="result-item">
                <div class="result-label">Block Number</div>
                <div class="result-value">${tx.blockNumber || 'N/A'}</div>
            </div>
            
            <div class="result-item">
                <div class="result-label">View on Explorer</div>
                <div class="result-value">
                    <a href="https://etherscan.io/tx/${tx.hash}" target="_blank" style="color: var(--primary-color);">
                        View on Etherscan →
                    </a>
                </div>
            </div>
        </div>
    `;
}

// OSINT Collection
document.getElementById('osintBtn')?.addEventListener('click', async () => {
    const address = document.getElementById('osintAddressInput').value.trim();
    
    if (!address) {
        showError('Please enter an address');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/osint`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ address })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayOSINTResults(data);
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to gather OSINT: ' + error.message);
    } finally {
        hideLoading();
    }
});

function displayOSINTResults(data) {
    const resultsDiv = document.getElementById('osintResults');
    resultsDiv.classList.remove('hidden');
    
    const osint = data.osint || {};
    const onChain = osint.on_chain_data || {};
    const labels = osint.public_labels || {};
    const threat = osint.threat_intelligence || {};
    const risk = osint.risk_assessment || {};
    
    resultsDiv.innerHTML = `
        <div class="fade-in">
            <h3 class="mb-3">OSINT Intelligence Report</h3>
            
            <!-- Risk Assessment -->
            <div class="result-item">
                <div class="result-label">Risk Assessment</div>
                <div class="result-value">
                    <span class="risk-badge ${getRiskBadgeClass(risk.risk_level || 'LOW')}">
                        ${risk.risk_level || 'LOW'}
                    </span>
                    <span style="margin-left: 1rem;">Score: ${risk.risk_score || 0}/100</span>
                    <div style="margin-top: 0.5rem; color: var(--text-secondary);">
                        ${risk.recommendation || ''}
                    </div>
                </div>
            </div>
            
            <!-- On-Chain Intelligence -->
            <div class="result-item">
                <div class="result-label">On-Chain Intelligence</div>
                <div class="result-value">
                    <div><strong>Type:</strong> ${onChain.address_type || 'Unknown'}</div>
                    <div><strong>First Seen:</strong> ${onChain.first_seen || 'N/A'}</div>
                    <div><strong>Last Seen:</strong> ${onChain.last_seen || 'N/A'}</div>
                    <div><strong>Total Transactions:</strong> ${onChain.total_transactions || 0}</div>
                    <div><strong>Unique Interactions:</strong> ${onChain.unique_interactions || 0}</div>
                </div>
            </div>
            
            <!-- Public Labels -->
            ${labels.etherscan_label || labels.known_entity ? `
                <div class="result-item">
                    <div class="result-label">Public Labels</div>
                    <div class="result-value">
                        ${labels.etherscan_label ? `<div><strong>Etherscan:</strong> ${labels.etherscan_label}</div>` : ''}
                        ${labels.known_entity ? `<div><strong>Known Entity:</strong> ${labels.known_entity}</div>` : ''}
                        ${labels.tags && labels.tags.length > 0 ? `<div><strong>Tags:</strong> ${labels.tags.join(', ')}</div>` : ''}
                    </div>
                </div>
            ` : ''}
            
            <!-- Threat Intelligence -->
            ${threat.is_flagged ? `
                <div class="result-item">
                    <div class="result-label">⚠️ Threat Intelligence</div>
                    <div class="result-value">
                        <div class="alert alert-danger">
                            This address has been flagged in threat databases!
                        </div>
                        ${threat.reports && threat.reports.length > 0 ? `
                            <div style="margin-top: 1rem;">
                                ${threat.reports.map(report => `
                                    <div style="margin-bottom: 0.5rem;">
                                        <strong>${report.type}:</strong> ${report.description}
                                    </div>
                                `).join('')}
                            </div>
                        ` : ''}
                    </div>
                </div>
            ` : ''}
            
            <!-- Risk Factors -->
            ${risk.risk_factors && risk.risk_factors.length > 0 ? `
                <div class="result-item">
                    <div class="result-label">Risk Factors</div>
                    <div class="result-value">
                        <ul style="list-style: none; padding: 0;">
                            ${risk.risk_factors.map(factor => `
                                <li style="margin-bottom: 0.5rem;">⚠️ ${factor}</li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            ` : ''}
            
            <!-- Download Report -->
            <div class="result-item">
                <button class="btn btn-secondary" onclick="downloadOSINTReport('${osint.address}')">
                    <i class="fas fa-download"></i>
                    Download Full Report
                </button>
            </div>
        </div>
    `;
}

async function downloadOSINTReport(address) {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/osint/report`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ address })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Create a blob and download
            const blob = new Blob([data.report], { type: 'text/markdown' });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `osint_report_${address.substring(0, 10)}.md`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to download report: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Recovery Plan Generation
document.getElementById('recoveryForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const incidentData = {
        victim_address: document.getElementById('victimAddress').value.trim(),
        attacker_address: document.getElementById('attackerAddress').value.trim(),
        amount_usd: parseFloat(document.getElementById('amountStolen').value),
        token_type: document.getElementById('tokenType').value,
        incident_date: document.getElementById('incidentDate').value,
        time_elapsed_hours: calculateHoursElapsed(document.getElementById('incidentDate').value)
    };
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/recovery/plan`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ incident_data: incidentData })
        });
        
        const data = await response.json();
        
        if (data.success) {
            displayRecoveryPlan(data.plan);
        } else {
            showError(data.error);
        }
    } catch (error) {
        showError('Failed to generate recovery plan: ' + error.message);
    } finally {
        hideLoading();
    }
});

function calculateHoursElapsed(incidentDate) {
    const incident = new Date(incidentDate);
    const now = new Date();
    return Math.floor((now - incident) / (1000 * 60 * 60));
}

function displayRecoveryPlan(plan) {
    const resultsDiv = document.getElementById('recoveryResults');
    resultsDiv.classList.remove('hidden');
    
    resultsDiv.innerHTML = `
        <div class="fade-in">
            <h3 class="mb-3">Recovery Plan</h3>
            
            <div class="alert alert-info">
                <strong>Incident ID:</strong> ${plan.incident_id}<br>
                <strong>Generated:</strong> ${new Date(plan.timestamp).toLocaleString()}
            </div>
            
            <!-- Recovery Probability -->
            <div class="result-item">
                <div class="result-label">Recovery Probability</div>
                <div class="result-value">
                    <span class="risk-badge ${getRiskBadgeClass(plan.recovery_probability.category)}">
                        ${plan.recovery_probability.category}
                    </span>
                    <span style="margin-left: 1rem;">${plan.recovery_probability.probability_score}%</span>
                    <div style="margin-top: 0.5rem; color: var(--text-secondary);">
                        ${plan.recovery_probability.description}
                    </div>
                </div>
            </div>
            
            <!-- Immediate Actions -->
            <div class="result-item">
                <div class="result-label">🚨 Immediate Actions (Within 1-4 hours)</div>
                <div class="result-value">
                    ${plan.immediate_actions.map((action, index) => `
                        <div style="margin-bottom: 1rem; padding: 1rem; background: var(--dark-bg); border-radius: 5px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <strong>${index + 1}. ${action.action}</strong>
                                <span class="risk-badge ${action.priority === 'CRITICAL' ? 'risk-critical' : 'risk-high'}">
                                    ${action.priority}
                                </span>
                            </div>
                            <div style="color: var(--text-secondary); margin-bottom: 0.5rem;">
                                ${action.description}
                            </div>
                            ${action.steps ? `
                                <ul style="margin-top: 0.5rem;">
                                    ${action.steps.map(step => `<li>${step}</li>`).join('')}
                                </ul>
                            ` : ''}
                            <div style="margin-top: 0.5rem; color: var(--warning-color);">
                                ⏰ Deadline: ${action.deadline}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <!-- Short-term Actions -->
            <div class="result-item">
                <div class="result-label">📋 Short-term Actions (24-48 hours)</div>
                <div class="result-value">
                    ${plan.short_term_actions.map((action, index) => `
                        <div style="margin-bottom: 1rem; padding: 1rem; background: var(--dark-bg); border-radius: 5px;">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <strong>${index + 1}. ${action.action}</strong>
                                <span class="risk-badge risk-medium">${action.priority}</span>
                            </div>
                            <div style="color: var(--text-secondary);">
                                ${action.description}
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <!-- Timeline -->
            <div class="result-item">
                <div class="result-label">⏱️ Estimated Timeline</div>
                <div class="result-value">
                    <div><strong>Best Case:</strong> ${plan.estimated_timeline.best_case}</div>
                    <div><strong>Typical Case:</strong> ${plan.estimated_timeline.typical_case}</div>
                    <div><strong>Worst Case:</strong> ${plan.estimated_timeline.worst_case}</div>
                    <div style="margin-top: 0.5rem; color: var(--text-secondary);">
                        ${plan.estimated_timeline.note}
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Load Prevention Tips on Page Load
async function loadPreventionTips() {
    try {
        const response = await fetch(`${API_BASE}/prevention`);
        const data = await response.json();
        
        if (data.success) {
            displayPreventionTips(data.recommendations);
        }
    } catch (error) {
        console.error('Failed to load prevention tips:', error);
    }
}

function displayPreventionTips(recommendations) {
    const tipsDiv = document.getElementById('preventionTips');
    
    tipsDiv.innerHTML = recommendations.map(category => `
        <div class="prevention-category">
            <h4>${category.category}</h4>
            <ul>
                ${category.recommendations.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>
    `).join('');
}

// Navigation
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', (e) => {
        e.preventDefault();
        
        // Update active state
        document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        
        // Scroll to section
        const target = link.getAttribute('href');
        document.querySelector(target).scrollIntoView({ behavior: 'smooth' });
    });
});

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    loadPreventionTips();
});