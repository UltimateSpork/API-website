/* --- 1. AUTHENTICATION & REDIRECTS --- */
(function checkAuth() {
    const token = localStorage.getItem("accessToken");
    const path = window.location.pathname;

    if (token && (path === "/login/" || path === "/")) {
        window.location.href = "/home/";
    } else if (!token && path !== "/login/") {
        window.location.href = "/login/";
    }
})();

const loginForm = document.getElementById('login-form');
if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/api/login/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem("accessToken", data.access);
                localStorage.setItem("refreshToken", data.refresh);
                window.location.href = "/home/";
            } else {
                alert("Login failed. Please check your credentials.");
            }
        } catch (error) {
            console.error("Auth error:", error);
        }
    });
}

/* --- 2. THE SMART FETCH (RETRY LOGIC) --- */
async function apiFetch(url, options = {}) {
    let token = localStorage.getItem("accessToken");

    options.headers = {
        ...options.headers,
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json",
    };

    let response = await fetch(url, options);

    if (response.status === 401) {
        const refresh = localStorage.getItem("refreshToken");
        if (!refresh) { logout(); return response; }

        const refreshResponse = await fetch("/api/token/refresh/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ refresh }),
        });

        if (refreshResponse.ok) {
            const data = await refreshResponse.json();
            localStorage.setItem("accessToken", data.access);
            options.headers["Authorization"] = `Bearer ${data.access}`;
            // Correctly re-fetch the original request with the new token
            response = await fetch(url, options); 
        } else {
            logout();
        }
    }
    return response;
}

/* --- 3. DATA LOADING & UI RENDERING --- */
async function loadEndpointData(endpointPath, elementId) {
    try {
        const response = await apiFetch(endpointPath);
        if (!response.ok) throw new Error("API call failed");
        const data = await response.json();
        renderToUI(elementId, data);
    } catch (error) {
        console.error(`Error loading ${endpointPath}:`, error);
        const container = document.getElementById(elementId);
        if (container) container.innerHTML = "<p class='text-red-500'>Error loading data.</p>";
    }
}

function renderToUI(elementId, data) {
    const container = document.getElementById(elementId);
    if (!container) return;

    if (!data || (Array.isArray(data) && data.length === 0)) {
        container.innerHTML = "<p>No records found.</p>";
        return;
    }

    // Handle single object responses (like 'total/') vs arrays
    const items = Array.isArray(data) ? data : [data];

    let html = '<ul class="divide-y divide-gray-200">';
    items.forEach(item => {
        // Dynamic label detection based on what the endpoint returns
        const label = item.countyName || item.stateName || item.name || item.commodity || item.year || item.landClass || item.description || "Total";
        const val = item.total_volume || item.volume || item.avg_volume || item.total || 0;
        
        html += `
            <li class="py-2 flex justify-between">
                <span class="font-medium">${label}</span>
                <span class="text-gray-600">${Number(val).toLocaleString()}</span>
            </li>`;
    });
    html += '</ul>';
    container.innerHTML = html;
}

/* --- 4. INITIALIZATION --- */
function logout() {
    localStorage.clear();
    window.location.href = "/login/";
}

document.addEventListener('DOMContentLoaded', () => {
    // Only run if the containers exist on this page
    if (document.getElementById("total-prod")) {
        loadEndpointData("/api/production/total/", "total-prod");
        loadEndpointData("/api/production/by-state/", "state-list");
        loadEndpointData("/api/production/by-county/", "county-list");
        loadEndpointData("/api/production/by-commodity/", "commodity-list");
        loadEndpointData("/api/production/average-year/", "avg-year");
        loadEndpointData("/api/production/offshore-onshore/", "offshore-box");
        loadEndpointData("/api/production/by-disposition/", "disposition-list");
        loadEndpointData("/api/production/top-counties/", "top-counties-box");
        loadEndpointData("/api/production/over-time/", "trends-box");
        loadEndpointData("/api/production/by-landclass/", "landclass-box");
    }
});


async function viewData(url) {
    try {
        const response = await apiFetch(url);
        const data = await response.json();

        // Show the hidden viewer
        const viewer = document.getElementById('data-viewer');
        const output = document.getElementById('json-output');
        
        viewer.classList.remove('hidden');
        
        // Pretty-print the JSON so it looks like the raw API data
        output.textContent = JSON.stringify(data, null, 4);
        
    } catch (error) {
        console.error("View Error:", error);
        alert("Could not load data. Ensure you are logged in.");
    }
}
