'use strict';

/* 최원영 : 100초마다 토큰 유효성 검사 */

const checkAuthorize = () => {
    const token = $.cookie('hello-token');
    if (!token) return location.reload();
};

setInterval(checkAuthorize(), 100);