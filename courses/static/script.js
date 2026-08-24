function showDetails(title, price, topics) {
    document.getElementById('modalTitle').innerText = title;
    document.getElementById('modalPrice').innerText = price;
    
    let topicsList = document.getElementById('modalTopics');
    topicsList.innerHTML = '';
    
    topics.forEach(function(topic) {
        let li = document.createElement('li');
        li.innerText = topic;
        topicsList.appendChild(li);
    });

    // تحديث رابط الواتساب ليشمل رسالة تلقائية باسم الكورس
    let whatsappPhone = "201107696040"; // تم إضافة كود مصر (20)
    let message = encodeURIComponent("مرحباً، أود الاستفسار والحجز في: " + title);
    document.getElementById('whatsappBtn').href = `https://wa.me/${whatsappPhone}?text=${message}`;

    document.getElementById('courseModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('courseModal').style.display = 'none';
}

// إغلاق النافذة عند الضغط خارجها
window.onclick = function(event) {
    let modal = document.getElementById('courseModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}