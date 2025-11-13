import { registry } from "@web/core/registry";
import { Component, useState, onWillStart } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class EstatePropertyDashboard extends Component {
    setup() {
        this.orm = useService("orm");
        this.action = useService("action");

        this.state = useState({
            totalProperties: 0,
            soldProperties: 0,
            propertyTypes: [],
            propertyStatus: [],
            recentProperties: [],
            currentPage: 1,
            itemsPerPage: 4,
            loading: true
        });

        onWillStart(async () => {
            await this.loadDashboardData();
        });

        console.log("✅ Real Estate Dashboard loaded!");
    }

    async loadDashboardData() {
        try {
            // Use ORM to fetch dashboard data directly
            await this.loadDashboardDataFallback();
        } catch (error) {
            console.error("Error loading dashboard data:", error);
            this.state.loading = false;
        }
    }

    async loadDashboardDataFallback() {
        try {
            // Fetch all properties
            const properties = await this.orm.searchRead(
                "estate.property",
                [],
                ["name", "expected_price", "selling_price", "state", "property_type_id", "image"]
            );

            // Calculate total properties
            this.state.totalProperties = properties.length;

            // Calculate sold properties
            this.state.soldProperties = properties.filter(p => p.state === 'sold').length;

            // Group by property type
            const typeGroups = {};
            properties.forEach(prop => {
                const typeName = prop.property_type_id ? prop.property_type_id[1] : 'Other';
                if (!typeGroups[typeName]) {
                    typeGroups[typeName] = 0;
                }
                typeGroups[typeName]++;
            });

            this.state.propertyTypes = Object.entries(typeGroups).map(([type, count]) => ({
                type,
                count,
                color: this.getRandomColor()
            }));

            // Group by state/status
            const statusGroups = {};
            const statusLabels = {
                'new': 'New',
                'offer_received': 'Offer Received',
                'offer_accepted': 'Offer Accepted',
                'sold': 'Sold',
                'canceled': 'Cancelled'
            };

            properties.forEach(prop => {
                const status = statusLabels[prop.state] || prop.state;
                if (!statusGroups[status]) {
                    statusGroups[status] = 0;
                }
                statusGroups[status]++;
            });

            this.state.propertyStatus = Object.entries(statusGroups).map(([status, count]) => ({
                status,
                count
            }));

            // Get recent properties (last 20)
            this.state.recentProperties = properties.slice(0, 20).map(prop => ({
                id: prop.id,
                name: prop.name,
                price: prop.selling_price || prop.expected_price,
                state: prop.state,
                stateLabel: statusLabels[prop.state] || prop.state,
                image: prop.image ? `data:image/png;base64,${prop.image}` : '/web/static/img/placeholder.png'
            }));

            this.state.loading = false;
        } catch (error) {
            console.error("Error loading dashboard data:", error);
            this.state.loading = false;
        }
    }

    getRandomColor() {
        const colors = ['#4A90E2', '#E24A4A', '#F5A623', '#50C878', '#9B59B6', '#E67E22'];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    getStatusColor(state) {
        const colors = {
            'sold': 'bg-success',
            'offer_accepted': 'bg-info',
            'offer_received': 'bg-primary',
            'canceled': 'bg-danger',
            'new': 'bg-secondary'
        };
        return colors[state] || 'bg-secondary';
    }

    getStatusBadgeClass(state) {
        const badges = {
            'sold': 'badge-success',
            'offer_accepted': 'badge-info',
            'offer_received': 'badge-primary',
            'canceled': 'badge-danger',
            'new': 'badge-secondary'
        };
        return badges[state] || 'badge-secondary';
    }

    async openPropertyForm(propertyId) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'estate.property',
            res_id: propertyId,
            views: [[false, 'form']],
            target: 'current',
        });
    }

    async createProperty() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'estate.property',
            views: [[false, 'form']],
            target: 'current',
        });
    }

    getPieChartPath(propertyType, index, total) {
        const percentage = propertyType.count / total;
        const angle = percentage * 360;

        // Calculate cumulative angle for this slice
        let cumulativeAngle = 0;
        for (let i = 0; i < index; i++) {
            cumulativeAngle += (this.state.propertyTypes[i].count / total) * 360;
        }

        const startAngle = cumulativeAngle;
        const endAngle = cumulativeAngle + angle;

        const x1 = 50 + 50 * Math.cos((startAngle * Math.PI) / 180);
        const y1 = 50 + 50 * Math.sin((startAngle * Math.PI) / 180);
        const x2 = 50 + 50 * Math.cos((endAngle * Math.PI) / 180);
        const y2 = 50 + 50 * Math.sin((endAngle * Math.PI) / 180);
        const largeArc = angle > 180 ? 1 : 0;

        return `M 50 50 L ${x1} ${y1} A 50 50 0 ${largeArc} 1 ${x2} ${y2} Z`;
    }

    getBarHeight(status) {
        const maxCount = Math.max(...this.state.propertyStatus.map(s => s.count), 1);
        return (status.count / maxCount) * 100;
    }

    // Pagination methods
    get paginatedProperties() {
        const startIndex = (this.state.currentPage - 1) * this.state.itemsPerPage;
        const endIndex = startIndex + this.state.itemsPerPage;
        return this.state.recentProperties.slice(startIndex, endIndex);
    }

    get totalPages() {
        return Math.ceil(this.state.recentProperties.length / this.state.itemsPerPage);
    }

    nextPage() {
        if (this.state.currentPage < this.totalPages) {
            this.state.currentPage++;
        }
    }

    prevPage() {
        if (this.state.currentPage > 1) {
            this.state.currentPage--;
        }
    }

    goToPage(page) {
        if (page >= 1 && page <= this.totalPages) {
            this.state.currentPage = page;
        }
    }

    handleImageError(event) {
        event.target.src = '/web/static/img/placeholder.png';
    }
}

EstatePropertyDashboard.template = "estate_property_dashboard_template";

registry.category("actions").add("estate_property_dashboard", EstatePropertyDashboard);