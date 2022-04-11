/*
    This script adds interactivity to the main navigation menu, including:
    - Allow menu to collapse/expand (be narrow/wide) on larger screens
    - Toggle visibility of entire nav menu on mobile devices
*/


// Get the value of a cookie by passing the cookie name
function getCookie(name) {
    // Convert cookies string to list
    var c_list = document.cookie.split("; "),
        i = 0,
        c,
        c_name,
        c_value;
    // Loop through cookies list to find a match
    for (i = 0; i < c_list.length; i++) {
        // Find cookie
        c = c_list[i].split('=');
        c_name = c[0];
        c_value = c[1];
        // Return cookie value if cookie name matches
        if (c_name === name) {
            return c_value;
        }
    }
    // If no cookie found with given name, return null
    return null;
}

// Set nav-collapsed class on pageload if found in cookies
// THIS MUST BE VANILLA JS, NOT JQUERY, AS JQUERY WAITS FOR PAGE TO FINISH LOADING, CAUSING A DELAY ON PAGE LOAD
if (getCookie('navCollapsed') == 1){
    document.getElementsByTagName('nav')[0].classList.add('nav-collapsed');
    document.getElementsByTagName('main')[0].classList.add('nav-collapsed');
    document.getElementById('nav-collapse').innerHTML = '<i class="fas fa-angle-double-right"></i>';
}

// The following is jQuery, as it's ok to wait for it to wait for page load
$(document).ready(function(){

    // Collapse/expand navigation bar (and update cookies, so setting can persist on page refresh)
    $('#nav-collapse').on('click', function(){
        // If nav already collapsed, expand
        if ($('nav').hasClass('nav-collapsed')){
            $('nav, main').removeClass('nav-collapsed');
            $(this).html('<i class="fas fa-angle-double-left"></i> Collapse');
            // Deletes cookie by setting date in the past
            document.cookie = "navCollapsed=; Thu, 01 Jan 1970 00:00:00 UTC; path=/; Secure;";
        }
        // If nav not collapsed, collapse it
        else {
            $('nav, main').addClass('nav-collapsed');
            $(this).html('<i class="fas fa-angle-double-right"></i>');
            // Set cookie
            document.cookie = "navCollapsed=1; expires=Mon, 31 Dec 2050 23:59:59 GMT; path=/; Secure;";
        }
    });

    // Toggle visibility of nav menu on small devices
    $('#nav-mobiletoggle').on('click', function(){
        $('nav').toggleClass('mobilevisible');
    });

});