const loggedIn=localStorage.getItem('loggedIn')==='true';
const navbar=document.getElementById('navbar');

if(loggedIn){
    navbar.innerHTML=`
        <a href="profile.html" class="text-blue-500 hover:underline">Profile</a>
        <a href="#" id="logout" class="text-blue-500 hover:underline">Logout</a>
    `;
} else {
    navbar.innerHTML=`
    <a href="login.html" class="text-blue-500 hover:underline">Login</a>
    <a href="signup.html" class="text-blue-500 hover:underline">Signup</a>
    `;
}