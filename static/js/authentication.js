'use strict';

/* 최원영 : 100초마다 토큰 유효성 검사 */

const checkAuthentication = () => {
    const token = $.cookie('hello-token');
    console.log(token);
    if (!token) return location.reload();
};

setInterval(checkAuthentication(), 100);