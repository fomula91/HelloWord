// set timt out
const alertRemove = (isReload) => {
    setTimeout(function () {
        $('#alart-content').remove();
        clearTimeout(alertRemove);
        isReload && location.reload();
    }, 1000);
};

// custom alert
const AlertDanger = (text, isReload) => {
    $('#alart').append(`
        <div id="alart-content" class="notification is-danger is-light" style="text-align: center;">
            ${text}
        </div>`);
    alertRemove(isReload);
};

const AlertSuccess = async (text, isReload) => {
    $('#alart').append(`
        <div id="alart-content" class="notification is-success is-light" style="text-align: center;">
            ${text}
        </div>`);
    alertRemove(isReload);
};