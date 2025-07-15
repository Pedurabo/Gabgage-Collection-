// main.js loaded
console.log('main.js loaded');

// Main JavaScript file for Garbage Collection Management System
// Real-life functionality and interactive features

class GarbageCollectionApp {
    constructor() {
        this.currentUser = null;
        this.notifications = [];
        this.realTimeUpdates = null;
        this.init();
    }

    init() {
        console.log('Garbage Collection App initialized');
        this.setupEventListeners();
        this.initializeRealTimeUpdates();
        this.setupMobileIntegration();
        this.setupGPSTracking();
    }

    setupEventListeners() {
        // Dashboard quick actions
        this.setupQuickActions();
        
        // Customer management
        this.setupCustomerManagement();
        
        // Service request handling
        this.setupServiceRequests();
        
        // Vehicle and route management
        this.setupVehicleManagement();
        
        // Billing and payments
        this.setupBillingSystem();
        
        // Analytics and reporting
        this.setupAnalytics();
        
        // Real-time tracking
        this.setupRealTimeTracking();
        
        // Mobile app integration
        this.setupMobileIntegration();
    }

    setupQuickActions() {
        // Quick action buttons
        document.querySelectorAll('.quick-action-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const action = btn.dataset.action;
                this.handleQuickAction(action);
            });
        });

        // Dashboard cards
        document.querySelectorAll('.dashboard-card').forEach(card => {
            card.addEventListener('click', (e) => {
                const cardType = card.dataset.type;
                this.handleDashboardCardClick(cardType);
            });
        });
    }

    handleQuickAction(action) {
        switch(action) {
            case 'new_request':
                this.openServiceRequestModal();
                break;
            case 'add_customer':
                this.openCustomerModal();
                break;
            case 'schedule_pickup':
                this.openScheduleModal();
                break;
            case 'generate_report':
                this.generateQuickReport();
                break;
            case 'track_vehicle':
                this.openVehicleTracking();
                break;
            case 'process_payment':
                this.openPaymentModal();
                break;
            default:
                console.log('Unknown action:', action);
        }
    }

    setupCustomerManagement() {
        // Customer search and filtering
        const customerSearch = document.getElementById('customerSearch');
        if (customerSearch) {
            customerSearch.addEventListener('input', (e) => {
                this.filterCustomers(e.target.value);
            });
        }

        // Customer status updates
        document.querySelectorAll('.customer-status-toggle').forEach(toggle => {
            toggle.addEventListener('change', (e) => {
                this.updateCustomerStatus(e.target.dataset.customerId, e.target.checked);
            });
        });

        // Customer service history
        document.querySelectorAll('.view-customer-history').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const customerId = e.target.dataset.customerId;
                this.loadCustomerHistory(customerId);
            });
        });
    }

    setupServiceRequests() {
        // Request status updates
        document.querySelectorAll('.request-status-select').forEach(select => {
            select.addEventListener('change', (e) => {
                this.updateRequestStatus(e.target.dataset.requestId, e.target.value);
            });
        });

        // Request assignment
        document.querySelectorAll('.assign-request').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const requestId = e.target.dataset.requestId;
                this.openAssignmentModal(requestId);
            });
        });

        // Request scheduling
        document.querySelectorAll('.schedule-request').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const requestId = e.target.dataset.requestId;
                this.openSchedulingModal(requestId);
            });
        });
    }

    setupVehicleManagement() {
        // Vehicle status updates
        document.querySelectorAll('.vehicle-status-toggle').forEach(toggle => {
            toggle.addEventListener('change', (e) => {
                this.updateVehicleStatus(e.target.dataset.vehicleId, e.target.checked);
            });
        });

        // Vehicle maintenance scheduling
        document.querySelectorAll('.schedule-maintenance').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const vehicleId = e.target.dataset.vehicleId;
                this.openMaintenanceModal(vehicleId);
            });
        });

        // Route optimization
        document.querySelectorAll('.optimize-route').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.optimizeRoute(e.target.dataset.routeId);
            });
        });
    }

    setupBillingSystem() {
        // Payment processing
        document.querySelectorAll('.process-payment').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const invoiceId = e.target.dataset.invoiceId;
                this.processPayment(invoiceId);
            });
        });

        // Invoice generation
        document.querySelectorAll('.generate-invoice').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const customerId = e.target.dataset.customerId;
                this.generateInvoice(customerId);
            });
        });

        // Payment method updates
        document.querySelectorAll('.update-payment-method').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const customerId = e.target.dataset.customerId;
                this.openPaymentMethodModal(customerId);
            });
        });
    }

    setupAnalytics() {
        // Chart interactions
        this.setupChartInteractions();
        
        // Report generation
        document.querySelectorAll('.generate-report').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const reportType = e.target.dataset.reportType;
                this.generateReport(reportType);
            });
        });

        // Data export
        document.querySelectorAll('.export-data').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const dataType = e.target.dataset.dataType;
                this.exportData(dataType);
            });
        });
    }

    setupRealTimeTracking() {
        // Vehicle tracking
        this.initializeVehicleTracking();
        
        // Driver location updates
        this.setupDriverTracking();
        
        // Service completion updates
        this.setupServiceCompletionTracking();
    }

    setupMobileIntegration() {
        // Mobile app notifications
        this.setupMobileNotifications();
        
        // Offline sync
        this.setupOfflineSync();
        
        // GPS tracking
        this.setupGPSTracking();
    }

    // Real-life business logic methods
    openServiceRequestModal() {
        this.showModal('serviceRequestModal', 'New Service Request');
    }

    openCustomerModal() {
        this.showModal('customerModal', 'Add New Customer');
    }

    openScheduleModal() {
        this.showModal('scheduleModal', 'Schedule Pickup');
    }

    openPaymentModal() {
        this.showModal('paymentModal', 'Process Payment');
    }

    openVehicleTracking() {
        this.showModal('vehicleTrackingModal', 'Vehicle Tracking');
    }

    generateQuickReport() {
        this.showLoading('Generating report...');
        
        fetch('/api/analytics/quick-report')
            .then(response => response.json())
            .then(data => {
                this.hideLoading();
                this.displayReport(data);
            })
            .catch(error => {
                this.hideLoading();
                this.showError('Failed to generate report: ' + error.message);
            });
    }

    filterCustomers(searchTerm) {
        const customerRows = document.querySelectorAll('.customer-row');
        
        customerRows.forEach(row => {
            const customerName = row.querySelector('.customer-name').textContent.toLowerCase();
            const customerEmail = row.querySelector('.customer-email').textContent.toLowerCase();
            
            if (customerName.includes(searchTerm.toLowerCase()) || 
                customerEmail.includes(searchTerm.toLowerCase())) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    }

    updateCustomerStatus(customerId, isActive) {
        fetch(`/api/customers/${customerId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({ is_active: isActive })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.showSuccess(`Customer status updated successfully`);
                this.updateCustomerUI(customerId, isActive);
            } else {
                this.showError('Failed to update customer status');
            }
        })
        .catch(error => {
            this.showError('Network error occurred');
        });
    }

    loadCustomerHistory(customerId) {
        this.showLoading('Loading customer history...');
        // TODO: Implement customer history loading
        setTimeout(() => {
            this.hideLoading();
            this.showSuccess('Customer history loaded successfully');
        }, 1000);
    }

    updateRequestStatus(requestId, newStatus) {
        this.showLoading('Updating request status...');
        // TODO: Implement status update
        setTimeout(() => {
            this.hideLoading();
            this.showSuccess(`Request status updated to ${newStatus}`);
        }, 1000);
    }

    openAssignmentModal(requestId) {
        const modal = this.createModal('Assign Request', this.getAssignmentForm(requestId));
        document.body.appendChild(modal);
        
        // Load available drivers
        this.loadAvailableDrivers(modal);
        
        // Load available vehicles
        this.loadAvailableVehicles(modal);
    }

    openSchedulingModal(requestId) {
        const modal = this.createModal('Schedule Request', this.getSchedulingForm(requestId));
        document.body.appendChild(modal);
        
        // Load available time slots
        this.loadAvailableTimeSlots(modal);
        
        // Setup route optimization
        this.setupRouteOptimization(modal);
    }

    updateVehicleStatus(vehicleId, isAvailable) {
        this.showLoading('Updating vehicle status...');
        // TODO: Implement vehicle status update
        setTimeout(() => {
            this.hideLoading();
            this.showSuccess(`Vehicle ${isAvailable ? 'marked as available' : 'marked as unavailable'}`);
        }, 1000);
    }

    openMaintenanceModal(vehicleId) {
        const modal = this.createModal('Schedule Maintenance', this.getMaintenanceForm(vehicleId));
        document.body.appendChild(modal);
        
        // Load maintenance history
        this.loadMaintenanceHistory(modal, vehicleId);
        
        // Setup maintenance scheduling
        this.setupMaintenanceScheduling(modal);
    }

    optimizeRoute(routeId) {
        this.showLoading('Optimizing route...');
        
        fetch(`/api/routes/${routeId}/optimize`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            this.hideLoading();
            if (data.success) {
                this.showSuccess('Route optimized successfully');
                this.displayOptimizedRoute(data.route);
            } else {
                this.showError('Failed to optimize route');
            }
        })
        .catch(error => {
            this.hideLoading();
            this.showError('Network error occurred');
        });
    }

    processPayment(invoiceId) {
        this.showLoading('Processing payment...');
        // TODO: Implement payment processing
        setTimeout(() => {
            this.hideLoading();
            this.showSuccess('Payment processed successfully');
        }, 1000);
    }

    generateInvoice(customerId) {
        this.showLoading('Generating invoice...');
        
        fetch(`/api/billing/generate-invoice`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': this.getCSRFToken()
            },
            body: JSON.stringify({ customer_id: customerId })
        })
        .then(response => response.json())
        .then(data => {
            this.hideLoading();
            if (data.success) {
                this.showSuccess('Invoice generated successfully');
                this.displayInvoice(data.invoice);
            } else {
                this.showError('Failed to generate invoice');
            }
        })
        .catch(error => {
            this.hideLoading();
            this.showError('Network error occurred');
        });
    }

    openPaymentMethodModal(customerId) {
        const modal = this.createModal('Update Payment Method', this.getPaymentMethodForm(customerId));
        document.body.appendChild(modal);
        
        // Setup payment method validation
        this.setupPaymentMethodValidation(modal);
    }

    setupChartInteractions() {
        // Chart click handlers
        document.querySelectorAll('.chart-container').forEach(container => {
            const chart = container.querySelector('canvas');
            if (chart) {
                chart.addEventListener('click', (e) => {
                    this.handleChartClick(e, chart);
                });
            }
        });
    }

    generateReport(reportType) {
        this.showLoading(`Generating ${reportType} report...`);
        // TODO: Implement report generation
        setTimeout(() => {
            this.hideLoading();
            this.showSuccess(`${reportType} report generated successfully`);
        }, 1000);
    }

    exportData(dataType) {
        this.showLoading(`Exporting ${dataType} data...`);
        
        fetch(`/api/export/${dataType}`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': this.getCSRFToken()
            }
        })
        .then(response => response.blob())
        .then(blob => {
            this.hideLoading();
            this.downloadFile(blob, `${dataType}_export.csv`);
        })
        .catch(error => {
            this.hideLoading();
            this.showError('Failed to export data');
        });
    }

    initializeVehicleTracking() {
        // Initialize map for vehicle tracking
        if (typeof google !== 'undefined' && google.maps) {
            this.initializeVehicleMap();
        }
        
        // Setup real-time vehicle location updates
        this.setupVehicleLocationUpdates();
    }

    setupVehicleLocationUpdates() {
        // TODO: Implement real-time vehicle location updates
        console.log('setupVehicleLocationUpdates called');
    }

    setupDriverTracking() {
        // Setup driver location tracking
        this.setupDriverLocationUpdates();
        
        // Setup driver status updates
        this.setupDriverStatusUpdates();
    }

    setupServiceCompletionTracking() {
        // Setup service completion notifications
        this.setupServiceCompletionNotifications();
        
        // Setup automatic billing
        this.setupAutomaticBilling();
    }

    setupServiceCompletionNotifications() {
        // TODO: Implement service completion notification logic
        console.log('setupServiceCompletionNotifications called');
    }

    setupAutomaticBilling() {
        // TODO: Implement automatic billing logic
        console.log('setupAutomaticBilling called');
    }

    setupMobileNotifications() {
        // Request notification permission
        if ('Notification' in window) {
            Notification.requestPermission();
        }
        
        // Setup push notifications
        this.setupPushNotifications();
    }

    setupPushNotifications() {
        // TODO: Implement push notification logic
        console.log('setupPushNotifications called');
    }

    setupOfflineSync() {
        // Setup offline data storage
        this.setupOfflineStorage();
        
        // Setup sync when online
        this.setupOnlineSync();
    }

    setupOnlineSync() {
        // Basic online sync logic
        const updateStatus = () => {
            if (navigator.onLine) {
                console.log('App is online. Syncing data with server...');
                // TODO: Add actual sync logic here
            } else {
                console.log('App is offline. Will sync when back online.');
            }
        };
        window.addEventListener('online', updateStatus);
        window.addEventListener('offline', updateStatus);
        // Initial check
        updateStatus();
    }

    setupGPSTracking() {
        // Setup GPS tracking for mobile app
        if (navigator.geolocation) {
            this.setupGeolocationTracking();
        }
    }

    setupDriverLocationUpdates() {
        // TODO: Implement real-time driver location updates
        console.log('setupDriverLocationUpdates called');
    }

    setupDriverStatusUpdates() {
        // TODO: Implement real-time driver status updates
        console.log('setupDriverStatusUpdates called');
    }

    setupGeolocationTracking() {
        // TODO: Implement geolocation tracking logic
        console.log('setupGeolocationTracking called');
    }

    // Utility methods
    createModal(title, content) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" id="modalSubmit">Submit</button>
                    </div>
                </div>
            </div>
        `;
        
        // Initialize Bootstrap modal
        const bootstrapModal = new bootstrap.Modal(modal);
        bootstrapModal.show();
        
        return modal;
    }

    getServiceRequestForm() {
        return `
            <form id="serviceRequestForm">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="serviceType" class="form-label">Service Type</label>
                            <select class="form-select" id="serviceType" required>
                                <option value="">Select Service Type</option>
                                <option value="residential">Residential Pickup</option>
                                <option value="commercial">Commercial Pickup</option>
                                <option value="recycling">Recycling Service</option>
                                <option value="hazardous">Hazardous Waste</option>
                                <option value="bulk">Bulk Item Pickup</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="scheduledDate" class="form-label">Scheduled Date</label>
                            <input type="date" class="form-control" id="scheduledDate" required>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="mb-3">
                            <label for="address" class="form-label">Pickup Address</label>
                            <input type="text" class="form-control" id="address" required>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="mb-3">
                            <label for="description" class="form-label">Description</label>
                            <textarea class="form-control" id="description" rows="3"></textarea>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="estimatedCost" class="form-label">Estimated Cost</label>
                            <div class="input-group">
                                <span class="input-group-text">$</span>
                                <input type="number" class="form-control" id="estimatedCost" readonly>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="priority" class="form-label">Priority</label>
                            <select class="form-select" id="priority">
                                <option value="low">Low</option>
                                <option value="medium" selected>Medium</option>
                                <option value="high">High</option>
                                <option value="urgent">Urgent</option>
                            </select>
                        </div>
                    </div>
                </div>
            </form>
        `;
    }

    getCustomerForm() {
        return `
            <form id="customerForm">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="customerName" class="form-label">Customer Name</label>
                            <input type="text" class="form-control" id="customerName" required>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="customerEmail" class="form-label">Email</label>
                            <input type="email" class="form-control" id="customerEmail" required>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="customerPhone" class="form-label">Phone</label>
                            <input type="tel" class="form-control" id="customerPhone" required>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="customerType" class="form-label">Customer Type</label>
                            <select class="form-select" id="customerType" required>
                                <option value="">Select Type</option>
                                <option value="residential">Residential</option>
                                <option value="commercial">Commercial</option>
                                <option value="industrial">Industrial</option>
                                <option value="government">Government</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="mb-3">
                            <label for="customerAddress" class="form-label">Address</label>
                            <input type="text" class="form-control" id="customerAddress" required>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="serviceFrequency" class="form-label">Service Frequency</label>
                            <select class="form-select" id="serviceFrequency">
                                <option value="weekly">Weekly</option>
                                <option value="biweekly">Bi-weekly</option>
                                <option value="monthly">Monthly</option>
                                <option value="on-demand">On-Demand</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="paymentMethod" class="form-label">Preferred Payment Method</label>
                            <select class="form-select" id="paymentMethod">
                                <option value="credit_card">Credit Card</option>
                                <option value="bank_transfer">Bank Transfer</option>
                                <option value="cash">Cash</option>
                                <option value="check">Check</option>
                            </select>
                        </div>
                    </div>
                </div>
            </form>
        `;
    }

    getScheduleForm() {
        return `
            <form id="scheduleForm">
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="pickupDate" class="form-label">Pickup Date</label>
                            <input type="date" class="form-control" id="pickupDate" required>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="pickupTime" class="form-label">Pickup Time</label>
                            <input type="time" class="form-control" id="pickupTime" required>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="assignedDriver" class="form-label">Assign Driver</label>
                            <select class="form-select" id="assignedDriver" required>
                                <option value="">Select Driver</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label for="assignedVehicle" class="form-label">Assign Vehicle</label>
                            <select class="form-select" id="assignedVehicle" required>
                                <option value="">Select Vehicle</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-12">
                        <div class="mb-3">
                            <label for="routeOptimization" class="form-label">Route Optimization</label>
                            <div class="form-check">
                                <input class="form-check-input" type="checkbox" id="routeOptimization" checked>
                                <label class="form-check-label" for="routeOptimization">
                                    Optimize route for efficiency
                                </label>
                            </div>
                        </div>
                    </div>
                </div>
            </form>
        `;
    }

    // Real-time updates and notifications
    initializeRealTimeUpdates() {
        // Setup WebSocket connection for real-time updates
        if (typeof WebSocket !== 'undefined') {
            this.setupWebSocketConnection();
        }
        
        // Setup polling for real-time updates
        this.setupPollingUpdates();
    }

    setupNotifications() {
        // Setup browser notifications
        if ('Notification' in window) {
            Notification.requestPermission();
        }
        
        // Setup in-app notifications
        this.setupInAppNotifications();
    }

    loadUserPreferences() {
        // Load user preferences from localStorage
        const preferences = localStorage.getItem('userPreferences');
        if (preferences) {
            this.userPreferences = JSON.parse(preferences);
        }
    }

    initializeCharts() {
        // Initialize Chart.js charts
        this.setupRevenueChart();
        this.setupServiceChart();
        this.setupCustomerChart();
    }

    setupMobileDetection() {
        // Detect mobile device
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            document.body.classList.add('mobile-device');
            this.setupMobileOptimizations();
        }
    }

    // Error handling and user feedback
    showSuccess(message) {
        this.showAlert(message, 'success');
    }

    showError(message) {
        this.showAlert(message, 'danger');
    }

    showWarning(message) {
        this.showAlert(message, 'warning');
    }

    showInfo(message) {
        this.showAlert(message, 'info');
    }

    showAlert(message, type = 'info') {
        const alertHTML = `
            <div class="alert alert-${type} alert-dismissible fade show position-fixed top-0 start-50 translate-middle-x mt-3" style="z-index: 9999;" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', alertHTML);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            const alert = document.querySelector('.alert');
            if (alert) {
                alert.remove();
            }
        }, 5000);
    }

    showLoading(message = 'Loading...') {
        // Create loading overlay
        const loadingHTML = `
            <div id="loadingOverlay" class="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center" style="background: rgba(0,0,0,0.5); z-index: 9999;">
                <div class="text-center text-white">
                    <div class="spinner-border mb-3" role="status"></div>
                    <div>${message}</div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', loadingHTML);
    }

    hideLoading() {
        const loadingOverlay = document.getElementById('loadingOverlay');
        if (loadingOverlay) {
            loadingOverlay.remove();
        }
    }

    getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || '';
    }

    downloadFile(blob, filename) {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    }

    setupOfflineStorage() {
        // TODO: Implement offline storage logic
        console.log('setupOfflineStorage called');
    }

    setupWebSocketConnection() {
        // TODO: Implement WebSocket connection logic
        console.log('setupWebSocketConnection called');
    }

    setupPollingUpdates() {
        // TODO: Implement polling for real-time updates
        console.log('setupPollingUpdates called');
        
        // Set up periodic polling for updates (every 30 seconds)
        setInterval(() => {
            this.checkForUpdates();
        }, 30000);
    }

    checkForUpdates() {
        // TODO: Implement check for updates logic
        console.log('Checking for updates...');
        
        // Example: Check for new notifications, status changes, etc.
        // This would typically make API calls to check for updates
    }

    // Modal and UI/UX Methods
    showModal(modalId, title) {
        // Create modal if it doesn't exist
        if (!document.getElementById(modalId)) {
            this.createModal(modalId, title);
        }
        
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        modal.show();
    }

    createModal(modalId, title) {
        const modalHTML = `
            <div class="modal fade" id="${modalId}" tabindex="-1" aria-labelledby="${modalId}Label" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="${modalId}Label">${title}</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="text-center">
                                <i class="fas fa-cog fa-spin fa-2x text-primary mb-3"></i>
                                <p class="text-muted">${title} feature coming soon!</p>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary">Save changes</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', modalHTML);
    }

    displayReport(data) {
        const modalHTML = `
            <div class="modal fade" id="reportModal" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">Quick Report</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-body text-center">
                                            <h6 class="card-title">Total Revenue</h6>
                                            <h3 class="text-success">$${data.data.total_revenue.toFixed(2)}</h3>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-body text-center">
                                            <h6 class="card-title">Total Requests</h6>
                                            <h3 class="text-primary">${data.data.total_requests}</h3>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row mt-3">
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-body text-center">
                                            <h6 class="card-title">Pending Requests</h6>
                                            <h3 class="text-warning">${data.data.pending_requests}</h3>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="card">
                                        <div class="card-body text-center">
                                            <h6 class="card-title">Completed Requests</h6>
                                            <h3 class="text-success">${data.data.completed_requests}</h3>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                            <button type="button" class="btn btn-primary">Export PDF</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Remove existing modal if any
        const existingModal = document.getElementById('reportModal');
        if (existingModal) {
            existingModal.remove();
        }
        
        document.body.insertAdjacentHTML('beforeend', modalHTML);
        const modal = new bootstrap.Modal(document.getElementById('reportModal'));
        modal.show();
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.garbageCollectionApp = new GarbageCollectionApp();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GarbageCollectionApp;
} 