'use strict';

/* 최원영 */

const logout = () => {
    $.removeCookie('hello-token');
    location.reload();
};

const wordsRender = (words) => {
    const wordsBox = $('#words-box');
    wordsBox.empty();
    words.forEach((word, i) => {
        const { _id, word_star, word_done, word_word, word_mean } = word;
        const starClickEvent = `wordStarClick('${_id}')`;
        const doneClickEvent = `wordDoneClick('${_id}')`;
        const editClickEvent = `wordEditClick('${_id}')`;
        const removeClickEvent = `wordRemoveClick('${_id}')`;
        const saveClickEvent = `wordSaveClick('${_id}');`;
        const cancelClickEvent = `wordEditCancel('${_id}')`;

        const doneImage = word_done ? checkFillIconImage : checkIconImage;
        const starImage = word_star ? starFillIconImage : starIconImage;

        const iconBox = `
                <div class="word-icons">
                <span id="${_id}-star" class="panel-icon icon-btn-right" onclick="${starClickEvent}">
                  ${starImage}
                </span>
                <span id="${_id}-done" class="panel-icon icon-btn-right" onclick="${doneClickEvent}">
                  ${doneImage}
                </span>
            </div>
        `;

        const textBox = `
            <div class="word-texts">
                <div class="word-span-box ${_id}-span">
                    ${word_word}
                </div>
                <div class="word-span-box ${_id}-span">
                    ${word_mean}
                </div>
                <div class="word-input-box ${_id}-input" hidden>
                    <input id="${_id}-word-edit" value="${word_word}">
                </div>
                <div class="word-input-box ${_id}-input" hidden>
                    <input id="${_id}-mean-edit" value="${word_mean}">
                </div>
            </div>
        `;

        const buttonBox = `
            <div class="word-buttons">
                <span class="panel-icon icon-btn-left ${_id}-edit-icon" onclick="${editClickEvent}">
                    ${editButtonIconImage}
                </span>
                <span class="panel-icon icon-btn-left ${_id}-remove-icon" onclick="${removeClickEvent}">
                    ${removeButtonIconImage}
                </span>
                <div class="panel-icon icon-btn-left ${_id}-save-icon" style="display: none;" onclick="${saveClickEvent}">
                    ${saveButtonIconImage}
                </div>
                <span class="panel-icon icon-btn-left ${_id}-cancel-icon" style="display: none;" onclick="${cancelClickEvent}">
                    ${cancelButtonIconImage}
                </span>
            </div>
        `;

        const box = `
              <div class="panel-block is-active">
                ${iconBox}
                ${textBox}
                ${buttonBox}
              </div>`;
        wordsBox.append(box);
    });
    return rows = [...words];
};

const filterRender = (index) => {
    const filterItems = $('#filter-items');
    filterItems.empty();

    const elements = [];
    filterState.map((state, i) => {
        const filterClickEvent = `filterRender(${i})`;
        const isCorrect = index === i;
        elements.push(`<a class="dropdown-item ${isCorrect && 'is-active'}"
                          onclick="${filterClickEvent}">
                            ${state.item}
                       </a>`);
        return { ...state, isActive: i === index };
    });
    const item = index !== undefined ? filterState[index].item : '필터';
    const query = index ? filterState[index].query : '';
    filterItems.append(elements.join(''));
    $('#filter-item').text(item);
    const queryString = query ? [`?${Object.keys(query)[0]}=${Object.values(query)[0]}`] : '';
    getWords(queryString);
};

const getWords = (query) => {
    $.ajax({
        type: "GET",
        url: `/api/words${query}`,
        success: (res) => {
            const { ok, words, message } = res;

            if (!ok) return AlertDanger(message);
            return wordsRender(words);
        }
    });
};

const filterToggle = () => {
    const dropDown = $("#filter-trigger");
    if (dropDown.attr("class").includes("is-active")) {
        return dropDown.removeClass('is-active');
    }
    return dropDown.addClass("is-active");
};

const wordAddClick = () => {
    const word_word = $('#new-word-word').val();
    const word_mean = $('#new-word-mean').val();

    if (word_word === "") return AlertDanger("단어를 입력하세요.");
    if (word_mean === "") return AlertDanger("뜻을 입력하세요.");

    $.ajax({
        type: "POST",
        url: "/api/words/new",
        data: { word_word, word_mean },
        success: (res) => {
            const { ok, message } = res;
            if (!ok) return AlertDanger(message);
            return AlertSuccess("등록되었습니다.", true);
        }
    });
};

const wordStarClick = (word_id) => {
    // JavaScript에 저장되어 있는 데이터에서 word_id에 해당하는 단어 검색]
    const word = rows.find(word => word._id === word_id);
    const { word_star } = word;
    const updated = !word_star;
    $.ajax({
        type: "PUT",
        url: `/api/words/${word_id}`,
        data: { word_star: updated },
        success: (res) => {
            const { ok, message } = res;
            if (!ok) return AlertDanger(message);

            rows[rows.indexOf(word)] = { ...word, word_star: updated }

            const span = $(`#${word_id}-star`);
            span.empty();
            span.append(!word_star ? starFillIconImage : starIconImage);
        }
    });
};

const wordDoneClick = (word_id) => {
    // JavaScript에 저장되어 있는 데이터에서 word_id에 해당하는 단어 검색
    const word = rows.find(word => word._id === word_id);
    const { word_done } = word;
    const updated = !word_done;
    $.ajax({
        type: "PUT",
        url: `/api/words/${word_id}`,
        data: { word_done: updated },
        success: (res) => {
            const { ok, message } = res;
            if (!ok) return AlertDanger(message);

            rows[rows.indexOf(word)] = { ...word, word_done: updated }

            const span = $(`#${word_id}-done`);
            span.empty();
            span.append(!word_done ? checkFillIconImage : checkIconImage);
        }
    });
};

const wordEditClick = (word_id) => {
    $(`.${word_id}-span`).hide();
    $(`.${word_id}-edit-icon`).hide();
    $(`.${word_id}-remove-icon`).hide();
    $(`.${word_id}-input`).show();
    $(`.${word_id}-save-icon`).show();
    $(`.${word_id}-cancel-icon`).show();
};

const wordEditCancel = (word_id) => {
    $(`.${word_id}-input`).hide();
    $(`.${word_id}-save-icon`).hide();
    $(`.${word_id}-cancel-icon`).hide();
    $(`.${word_id}-span`).show();
    $(`.${word_id}-edit-icon`).show();
    $(`.${word_id}-remove-icon`).show();
};

const wordRemoveClick = (word_id) => {
    const question = "단어를 삭제하시겠습니까?";
    if (confirm(question)) {
        $.ajax({
            type: "DELETE",
            url: `/api/words/${word_id}`,
            success: (res) => {
                const { ok, message } = res;
                if (!ok) return AlertDanger(message);
                return AlertSuccess("삭제되었습니다.", true);
            }
        });
    };
};

const wordSaveClick = (word_id) => {
    const word_word = $(`#${word_id}-word-edit`).val();
    const word_mean = $(`#${word_id}-mean-edit`).val();

    if (!word_word) return AlertDanger("단어를 입력하세요.");
    if (!word_mean) return AlertDanger("뜻을 입력하세요.");

    const origin = rows.find(word => word._id === word_id);
    if (origin.word_word === word_word && origin.word_mean === word_mean) {
        return wordEditCancel(word_id);
    };

    $.ajax({
        type: "PUT",
        url: `/api/words/${word_id}`,
        data: { word_word, word_mean },
        success: (res) => {
            const { ok, message } = res;
            if (!ok) return AlertDanger(message);
            return AlertSuccess("저장되었습니다.", true);
        }
    });
};

$(document).ready(() => {
    filterRender();
});
