

    /*
    ==================================================
    VISIONEDGE API CONFIGURATION
    ==================================================
    */

    const API_BASE_URL = "http://localhost:5000";


    /*
    ==================================================
    INITIALIZE AOS
    ==================================================
    */

    document.addEventListener("DOMContentLoaded", function () {

        if (typeof AOS !== "undefined") {
            AOS.init({
                duration: 800,
                once: true
            });
        }

        if (window.location.hash === '#otpModal') {
            const modalEl = document.getElementById('otpLoginModal');
            if (modalEl) {
                const modal = new bootstrap.Modal(modalEl);
                modal.show();
            }
        }

    });


    /*
    ==================================================
    PASSWORD SHOW / HIDE
    ==================================================
    */

    const togglePasswordBtn =
        document.getElementById("togglePasswordBtn");

    const pwdInput =
        document.getElementById("pwdInput");

    const eyeIcon =
        document.getElementById("eyeIcon");


    togglePasswordBtn.addEventListener(
        "click",
        function () {

            if (pwdInput.type === "password") {

                pwdInput.type = "text";

                eyeIcon.classList.remove("bi-eye");

                eyeIcon.classList.add("bi-eye-slash");

                togglePasswordBtn.setAttribute(
                    "aria-label",
                    "Hide password"
                );

            } else {

                pwdInput.type = "password";

                eyeIcon.classList.remove("bi-eye-slash");

                eyeIcon.classList.add("bi-eye");

                togglePasswordBtn.setAttribute(
                    "aria-label",
                    "Show password"
                );

            }

        }
    );


    /*
    ==================================================
    SHOW LOGIN MESSAGE
    ==================================================
    */

    function showLoginMessage(
        message,
        type = "danger"
    ) {

        const loginMessage =
            document.getElementById("loginMessage");


        loginMessage.className =
            "alert alert-" + type;


        loginMessage.textContent =
            message;


        loginMessage.style.display =
            "block";

    }


    /*
    ==================================================
    HIDE LOGIN MESSAGE
    ==================================================
    */

    function hideLoginMessage() {

        const loginMessage =
            document.getElementById("loginMessage");


        loginMessage.style.display =
            "none";

    }


    /*
    ==================================================
    LOGIN FORM SUBMISSION
    ==================================================
    */

    const loginForm =
        document.getElementById("loginForm");


    loginForm.addEventListener(
        "submit",
        async function (event) {

            event.preventDefault();


            hideLoginMessage();


            /*
            ------------------------------------------
            GET FORM DATA
            ------------------------------------------
            */

            const username =
                document
                    .getElementById("username")
                    .value
                    .trim();


            const password =
                document
                    .getElementById("pwdInput")
                    .value;


            const rememberMe =
                document
                    .getElementById("rememberMe")
                    .checked;


            /*
            ------------------------------------------
            VALIDATION
            ------------------------------------------
            */

            if (!username || !password) {

                showLoginMessage(
                    "Please enter your username and password.",
                    "warning"
                );

                return;

            }


            /*
            ------------------------------------------
            LOGIN BUTTON LOADING STATE
            ------------------------------------------
            */

            const loginBtn =
                document.getElementById("loginBtn");

            const loginBtnText =
                document.getElementById("loginBtnText");

            const loginSpinner =
                document.getElementById("loginSpinner");


            loginBtn.disabled =
                true;

            loginBtn.classList.add(
                "login-loading"
            );

            loginBtnText.textContent =
                "Logging in...";

            loginSpinner.classList.remove(
                "d-none"
            );


            try {

                /*
                --------------------------------------
                SEND LOGIN REQUEST TO FLASK
                --------------------------------------
                */

                const response =
                    await fetch(
                        API_BASE_URL + "/api/auth/login",
                        {
                            method: "POST",

                            headers: {
                                "Content-Type":
                                    "application/json"
                            },

                            body: JSON.stringify({

                                username:
                                    username,

                                password:
                                    password

                            })
                        }
                    );


                /*
                --------------------------------------
                GET SERVER RESPONSE
                --------------------------------------
                */

                const data =
                    await response.json();


                /*
                --------------------------------------
                LOGIN FAILED
                --------------------------------------
                */

                if (!response.ok) {

                    showLoginMessage(
                        data.message ||
                        "Invalid username or password.",
                        "danger"
                    );

                    return;

                }


                /*
                --------------------------------------
                LOGIN SUCCESSFUL
                --------------------------------------
                */

                if (
                    data.access_token
                ) {


                    /*
                    ----------------------------------
                    SAVE JWT TOKEN
                    ----------------------------------
                    */

                    localStorage.setItem(
                        "access_token",
                        data.access_token
                    );


                    /*
                    ----------------------------------
                    SAVE USER DATA
                    ----------------------------------
                    */

                    if (data.user) {

                        const userData =
                            JSON.stringify(
                                data.user
                            );


                        localStorage.setItem(
                            "current_user",
                            userData
                        );

                    }


                    /*
                    ----------------------------------
                    SUCCESS MESSAGE
                    ----------------------------------
                    */

                    showLoginMessage(
                        "Login successful! Redirecting...",
                        "success"
                    );


                    /*
                    ----------------------------------
                    REDIRECT
                    ----------------------------------
                    */

                    setTimeout(
                        function () {

                            window.location.href =
                                "dashboard.html";

                        },
                        800
                    );

                } else {

                    showLoginMessage(
                        "Login failed. Token was not received.",
                        "danger"
                    );

                }


            } catch (error) {

                console.error(
                    "Login Error:",
                    error
                );


                showLoginMessage(
                    "Unable to connect to the VisionEdge server. Please make sure the backend is running.",
                    "danger"
                );


            } finally {

                /*
                --------------------------------------
                RESET LOGIN BUTTON
                --------------------------------------
                */

                loginBtn.disabled =
                    false;

                loginBtn.classList.remove(
                    "login-loading"
                );

                loginBtnText.textContent =
                    "Log In";

                loginSpinner.classList.add(
                    "d-none"
                );

            }

        }
    );


    /*
    ==================================================
    GOOGLE LOGIN
    ==================================================
    */

    document
        .getElementById("googleLoginBtn")
        .addEventListener(
            "click",
            function () {

                showLoginMessage(
                    "Google Login will be connected after Google OAuth is configured.",
                    "info"
                );
            }
        );

    /*
    ==================================================
    PHONE OTP LOGIN / SIGNUP LOGIC
    ==================================================
    */
    let currentOtpPhone = "";

    function showOtpAlert(msg, type = "danger") {
        const el = document.getElementById("otpModalAlert");
        el.className = `alert alert-${type} py-2 small mb-3`;
        el.textContent = msg;
        el.classList.remove("d-none");
    }

    function hideOtpAlert() {
        document.getElementById("otpModalAlert").classList.add("d-none");
    }

    // SEND OTP
    window.handleSendOtp = async function() {
        hideOtpAlert();
        const phoneInput = document.getElementById("otpPhoneInput").value.trim();
        if (!phoneInput || phoneInput.length < 10) {
            showOtpAlert("Please enter a valid 10-digit mobile number.", "warning");
            return;
        }

        currentOtpPhone = phoneInput;
        const btn = document.getElementById("sendOtpBtn");
        const spinner = document.getElementById("sendOtpSpinner");
        btn.disabled = true;
        spinner.classList.remove("d-none");

        try {
            const res = await fetch(API_BASE_URL + "/api/auth/send-otp", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ phone: phoneInput })
            });

            const data = await res.json();
            if (!res.ok) {
                showOtpAlert(data.message || "Failed to send OTP.", "danger");
                return;
            }

            document.getElementById("displayPhone").textContent = "+91 " + phoneInput;
            if (data.otp) {
                document.getElementById("demoOtpBadge").textContent = "Demo OTP: " + data.otp;
                document.getElementById("otpCodeInput").value = data.otp; // Auto fill test OTP
            }

            document.getElementById("otpStep1").classList.add("d-none");
            document.getElementById("otpStep2").classList.remove("d-none");
            showOtpAlert("OTP sent successfully! Enter code below.", "success");
        } catch (err) {
            showOtpAlert("Network error. Make sure the backend server is running.", "danger");
        } finally {
            btn.disabled = false;
            spinner.classList.add("d-none");
        }
    };

    // VERIFY OTP
    window.handleVerifyOtp = async function() {
        hideOtpAlert();
        const otpCode = document.getElementById("otpCodeInput").value.trim();
        const firstName = document.getElementById("otpFirstName").value.trim();
        const lastName = document.getElementById("otpLastName").value.trim();

        if (!otpCode) {
            showOtpAlert("Please enter the 6-digit verification code.", "warning");
            return;
        }

        const btn = document.getElementById("verifyOtpBtn");
        const spinner = document.getElementById("verifyOtpSpinner");
        btn.disabled = true;
        spinner.classList.remove("d-none");

        try {
            const res = await fetch(API_BASE_URL + "/api/auth/verify-otp", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    phone: currentOtpPhone,
                    otp: otpCode,
                    first_name: firstName,
                    last_name: lastName
                })
            });

            const data = await res.json();
            if (!res.ok) {
                showOtpAlert(data.message || "Invalid OTP code.", "danger");
                return;
            }

            if (data.access_token) {
                localStorage.setItem("access_token", data.access_token);
                if (data.user) {
                    localStorage.setItem("current_user", JSON.stringify(data.user));
                }

                showOtpAlert("Login successful! Redirecting...", "success");
                setTimeout(() => {
                    window.location.href = "dashboard.html";
                }, 800);
            }
        } catch (err) {
            showOtpAlert("Failed to verify OTP. Server connection error.", "danger");
        } finally {
            btn.disabled = false;
            spinner.classList.add("d-none");
        }
    };

    // RESEND OTP
    window.handleResendOtp = function() {
        document.getElementById("otpStep2").classList.add("d-none");
        document.getElementById("otpStep1").classList.remove("d-none");
        hideOtpAlert();
    };

