const buggerMenuClick = () => {
    const buggerMenu = $(".navbar-burger");
    const navbarMenu = $(".navbar-menu");

    if (buggerMenu.attr("class").includes("is-active")) {
        navbarMenu.removeClass("is-active");
        return buggerMenu.removeClass('is-active');
    }

    navbarMenu.addClass("is-active");
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