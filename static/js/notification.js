// Notification
// ------------
const notificationMarkAsReadAll = document.querySelector('.dropdown-notifications-all');
const notificationMarkAsReadList = document.querySelectorAll('.dropdown-notifications-read');

// Notification: Mark as all as read
if (notificationMarkAsReadAll) {
    notificationMarkAsReadAll.addEventListener('click', event => {
        readNotification('all')
        notificationMarkAsReadList.forEach(item => {
            item.closest('.dropdown-notifications-item').classList.add('marked-as-read');
        });
    });
}
// Notification: Mark as read/unread onclick of dot
if (notificationMarkAsReadList) {
    notificationMarkAsReadList.forEach(item => {
        item.addEventListener('click', event => {
            readNotification(item.dataset.id)
            item.closest('.dropdown-notifications-item').classList.toggle('marked-as-read');
        });
    });
}

// Notification: Mark as read/unread onclick of dot
const notificationArchiveMessageList = document.querySelectorAll('.dropdown-notifications-archive');
notificationArchiveMessageList.forEach(item => {
    item.addEventListener('click', event => {
        item.closest('.dropdown-notifications-item').remove();
    });
});


async function readNotification(id) {
    url = '/fetch/notification-read/'
    response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'id': id })
    })

    data = response.json()
}