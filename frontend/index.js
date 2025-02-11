document.addEventListener('DOMContentLoaded', function() {
    // 检查登录状态
    checkLoginStatus();

    // 加载统计数据
    loadDashboardStats();

    // 加载最近活动
    loadRecentActivities();

    // 绑定导航栏事件
    document.getElementById('logoutLink').addEventListener('click', logout);
});

function checkLoginStatus() {
    fetch('/prjeventsys/v1/auth/status')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.logged_in) {
                document.getElementById('username').textContent = data.empname;
            } else {
                // 只有在确实未登录时才跳转
                if (window.location.pathname !== '/login.html') {
                    window.location.href = '/login.html';
                }
            }
        })
        .catch(error => {
            console.error('检查登录状态失败:', error);
            // 只有在当前页面不是登录页时才跳转
            if (window.location.pathname !== '/login.html') {
                window.location.href = '/login.html';
            }
        });
}

function loadDashboardStats() {
    // 获取项目总数
    fetch('/prjeventsys/v1/project/count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('projectCount').textContent = data.count;
        });

    // 获取待处理事件数
    fetch('/prjeventsys/v1/event/pending_count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('pendingEvents').textContent = data.count;
        });

    // 获取在线用户数
    fetch('/prjeventsys/v1/user/online_count')
        .then(response => response.json())
        .then(data => {
            document.getElementById('onlineUsers').textContent = data.count;
        });
}

function loadRecentActivities() {
    fetch('/prjeventsys/v1/activity/recent')
        .then(response => response.json())
        .then(data => {
            const activityList = document.getElementById('activityList');
            activityList.innerHTML = data.activities.map(activity => `
                <li>
                    <strong>${activity.type}</strong>: ${activity.description}
                    <span class="time">${activity.time}</span>
                </li>
            `).join('');
        });
}

function logout() {
    fetch('/prjeventsys/v1/auth/logout', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/login.html';
        }
    });
} 