// 1. استبدلي هذه البيانات ببيانات مشروعك من Firebase Console
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT_ID.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// تهيئة Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();

let isLoginMode = true;

function toggleAuthMode() {
    isLoginMode = !isLoginMode;
    document.getElementById('authTitle').innerText = isLoginMode ? "تسجيل الدخول" : "حساب جديد";
    document.getElementById('submitBtn').innerText = isLoginMode ? "دخول" : "إنشاء حساب";
    document.getElementById('toggleText').innerHTML = isLoginMode 
        ? 'ليس لديك حساب؟ <span onclick="toggleAuthMode()">إنشاء حساب جديد</span>'
        : 'لديك حساب بالفعل؟ <span onclick="toggleAuthMode()">تسجيل الدخول</span>';
    document.getElementById('errorBox').innerText = '';
}

document.getElementById('authForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const email = document.getElementById('emailInput').value;
    const password = document.getElementById('passwordInput').value;
    const errorBox = document.getElementById('errorBox');
    errorBox.innerText = '';

    if (isLoginMode) {
        // تسجيل الدخول
        auth.signInWithEmailAndPassword(email, password)
            .then((userCredential) => {
                window.location.href = "dashboard.html";
            })
            .catch((error) => {
                errorBox.innerText = "خطأ: البريد الإلكتروني أو كلمة السر غير صحيحة";
            });
    } else {
        // إنشاء حساب جديد
        auth.createUserWithEmailAndPassword(email, password)
            .then((userCredential) => {
                alert("تم إنشاء الحساب بنجاح!");
                window.location.href = "dashboard.html";
            })
            .catch((error) => {
                errorBox.innerText = "خطأ: " + error.message;
            });
    }
});