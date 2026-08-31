document.addEventListener('DOMContentLoaded', () => {
    const runBtn = document.getElementById('runBtn');
    
    fetchMetrics();
    fetchRuns();

    runBtn.addEventListener('click', async () => {
        runBtn.disabled = true;
        runBtn.innerHTML = '<span class="btn-icon">⌛</span> Orchestrating Agent...';
        
        try {
            const res = await fetch('/api/run-orchestrator', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cluster_name: 'prod-core-cluster' })
            });
            const data = await res.json();
            
            updateLatestRunUI(data);
            await fetchMetrics();
            await fetchRuns();
        } catch (err) {
            console.error('Failed to run orchestrator:', err);
            alert('Failed to trigger FinOps Autopilot workflow.');
        } finally {
            runBtn.disabled = false;
            runBtn.innerHTML = '<span class="btn-icon">⚡</span> Run FinOps Autopilot';
        }
    });
});

async function fetchMetrics() {
    try {
        const res = await fetch('/api/metrics');
        const data = await res.json();

        document.getElementById('kpiSpend').textContent = `$${data.monthly_cloud_spend.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('kpiSavingsMo').textContent = `$${data.savings_identified_monthly.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('kpiSavingsYr').textContent = `$${data.savings_identified_annual.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
        document.getElementById('kpiOptCount').textContent = data.optimizations_found;
        document.getElementById('kpiPrCount').textContent = data.prs_created;
        document.getElementById('kpiPassRate').textContent = `${data.validation_pass_rate}%`;
        document.getElementById('demoModeBadge').textContent = `DEMO_MODE=${data.demo_mode}`;
    } catch (e) {
        console.error('Error fetching metrics:', e);
    }
}

async function fetchRuns() {
    try {
        const res = await fetch('/api/runs');
        const runs = await res.json();
        
        if (runs && runs.length > 0) {
            updateLatestRunUI(runs[0]);
            renderHistoryTable(runs);
        }
    } catch (e) {
        console.error('Error fetching runs:', e);
    }
}

function updateLatestRunUI(run) {
    document.getElementById('runStatusPill').textContent = run.status;
    document.getElementById('metaResource').textContent = run.resource || 'prod-core-cluster';
    document.getElementById('metaExecutionId').textContent = run.execution_id;
    document.getElementById('metaConfidence').textContent = `${(run.confidence * 100).toFixed(0)}%`;
    
    if (run.finding) {
        document.getElementById('findingText').textContent = run.finding;
    }

    if (run.projected_monthly_savings) {
        document.getElementById('sidebarMonthly').textContent = `$${run.projected_monthly_savings.toLocaleString('en-US', {minimumFractionDigits: 0})}`;
        document.getElementById('sidebarAnnual').textContent = `$${run.projected_annual_savings.toLocaleString('en-US', {minimumFractionDigits: 0})} / year`;
    }

    if (run.old_configuration && run.old_configuration.node_count) {
        document.getElementById('oldNodeCount').textContent = `${run.old_configuration.node_count} nodes`;
    }
    if (run.new_configuration && run.new_configuration.node_count) {
        document.getElementById('newNodeCount').textContent = `${run.new_configuration.node_count} nodes`;
    }

    if (run.github_pr) {
        document.getElementById('prLink').textContent = run.github_pr.title || '🤖 FinOps Autopilot PR';
        document.getElementById('prLink').href = run.github_pr.pr_url || '#';
        document.getElementById('prBranch').textContent = run.github_pr.branch_name || 'finops/gke-rightsize';
    }
    if (run.cloud_build_id) {
        document.getElementById('prBuildId').textContent = run.cloud_build_id;
    }
}

function renderHistoryTable(runs) {
    const tbody = document.getElementById('historyTableBody');
    tbody.innerHTML = '';

    runs.forEach(r => {
        const tr = document.createElement('tr');
        const prUrl = r.github_pr ? r.github_pr.pr_url : '#';
        const prNum = r.github_pr ? `#${r.github_pr.pr_number}` : 'N/A';
        const buildId = r.cloud_build_id || 'N/A';

        tr.innerHTML = `
            <td><code class="mono">${r.execution_id}</code></td>
            <td>${r.resource}</td>
            <td><span class="status-pill status-completed">${r.status}</span></td>
            <td class="badge-new">$${r.projected_monthly_savings.toFixed(2)}</td>
            <td class="badge-new">$${r.projected_annual_savings.toFixed(2)}</td>
            <td>${(r.confidence * 100).toFixed(0)}%</td>
            <td><a href="${prUrl}" target="_blank" class="pr-link">${prNum}</a></td>
            <td><code class="mono">${buildId}</code></td>
        `;
        tbody.appendChild(tr);
    });
}
