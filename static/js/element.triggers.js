const buggerMenuClick = () => {
    const buggerMenu = $("#bugger-menu");
    const navbarMenu = $(".navbar-menu");

    if (buggerMenu.attr("class").includes("is-active")) {
        navbarMenu.hide();
        return buggerMenu.removeClass('is-active');
    }
    navbarMenu.show();
    return buggerMenu.addClass("is-active");
}

const mobileDropDownClick = () => {
    const dropDownButton = $('.navbar-link');
    const dropDownItmes = $('.navbar-dropdown');

    if (dropDownButton.attr("class").includes("is-active")) {
        dropDownItmes.hide();
        return dropDownButton.removeClass('is-active');
    }
    dropDownItmes.show();
    return dropDownButton.addClass("is-active");
}