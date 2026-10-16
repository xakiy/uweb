/**
 * Analytics Dashboard Charts
 * Self-contained charting module for the analytics dashboard
 */

(function() {
    'use strict';

    // Chart configuration
    const CHART_COLORS = {
        primary: 'rgb(75, 192, 192)',
        secondary: 'rgb(54, 162, 235)',
        success: 'rgb(75, 201, 107)',
        warning: 'rgb(255, 206, 86)',
        danger: 'rgb(255, 99, 132)',
        info: 'rgb(23, 162, 184)'
    };

    /**
     * Initialize daily views line chart
     */
    function initDailyViewsChart(ctx, data) {
        if (!ctx || !data || data.length === 0) return;

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.map(d => d.timestamp),
                datasets: [{
                    label: 'Views',
                    data: data.map(d => d.view_count || d.count),
                    borderColor: CHART_COLORS.primary,
                    backgroundColor: 'rgba(75, 192, 192, 0.1)',
                    tension: 0.1,
                    fill: true,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.y + ' views';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }

    /**
     * Initialize top pages bar chart
     */
    function initTopPagesChart(ctx, data) {
        if (!ctx || !data || data.length === 0) return;

        const colors = [
            CHART_COLORS.primary,
            CHART_COLORS.secondary,
            CHART_COLORS.success,
            CHART_COLORS.warning,
            CHART_COLORS.danger,
            CHART_COLORS.info,
            'rgb(153, 102, 255)',
            'rgb(255, 159, 64)',
            'rgb(199, 199, 199)',
            'rgb(84, 170, 216)'
        ];

        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.map(d => d.page_title),
                datasets: [{
                    label: 'Views',
                    data: data.map(d => d.view_count),
                    backgroundColor: colors.slice(0, data.length),
                    borderColor: colors.slice(0, data.length).map(c => c.replace('rgb', 'rgba').replace(')', ', 1)')),
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.parsed.y + ' views';
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }

    /**
     * Initialize referrer pie chart
     */
    function initReferrerChart(ctx, data) {
        if (!ctx || !data || data.length === 0) return;

        const colors = [
            CHART_COLORS.primary,
            CHART_COLORS.secondary,
            CHART_COLORS.success,
            CHART_COLORS.warning,
            CHART_COLORS.danger,
            CHART_COLORS.info,
            'rgb(153, 102, 255)',
            'rgb(255, 159, 64)',
            'rgb(199, 199, 199)',
            'rgb(84, 170, 216)'
        ];

        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(d => d.referrer),
                datasets: [{
                    data: data.map(d => d.count),
                    backgroundColor: colors.slice(0, data.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            boxWidth: 12
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((context.parsed / total) * 100);
                                return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                            }
                        }
                    }
                }
            }
        });
    }

    // Expose functions globally
    window.AnalyticsCharts = {
        initDailyViewsChart,
        initTopPagesChart,
        initReferrerChart
    };

    /**
     * Safely parse JSON from a json_script-generated <script> element.
     */
    function parseJsonScript(elementId) {
        const el = document.getElementById(elementId);
        if (!el) return [];
        try {
            const parsed = JSON.parse(el.textContent);
            return Array.isArray(parsed) ? parsed : [];
        } catch (e) {
            console.warn('Analytics: failed to parse chart data from', elementId, ':', e);
            return [];
        }
    }

    // Auto-initialize on DOM ready
    document.addEventListener('DOMContentLoaded', function() {
        // Daily views chart
        const dailyCtx = document.getElementById('dailyViewsChart');
        if (dailyCtx) {
            const dailyData = parseJsonScript('daily-views-data');
            initDailyViewsChart(dailyCtx.getContext('2d'), dailyData);
        }

        // Top pages chart
        const topPagesCtx = document.getElementById('topPagesChart');
        if (topPagesCtx) {
            const topPagesData = parseJsonScript('top-pages-data');
            initTopPagesChart(topPagesCtx.getContext('2d'), topPagesData);
        }

        // Referrer chart (page_analytics view)
        const referrerCtx = document.getElementById('referrerChart');
        if (referrerCtx) {
            const referrerData = parseJsonScript('referrers-data');
            initReferrerChart(referrerCtx.getContext('2d'), referrerData);
        }

        // Daily chart (page_analytics view)
        const dailyChartCtx = document.getElementById('dailyChart');
        if (dailyChartCtx) {
            const dailyChartData = parseJsonScript('daily-data');
            initDailyViewsChart(dailyChartCtx.getContext('2d'), dailyChartData);
        }
    });

})();
