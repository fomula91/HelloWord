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
        const {word_id, word_star, word_done, word_word, word_mean } = word;
        const starClickEvent = `wordStarClick('${word_id}')`;
        const doneClickEvent = `wordDoneClick('${word_id}')`;
        const editClickEvent = `wordEditClick('${word_id}')`;
        const removeClickEvent = `wordRemoveClick('${word_id}')`;
        const saveClickEvent = `wordSaveClick('${word_id}');`;
        const cancelClickEvent = `wordEditCancel('${word_id}')`;

        const doneImage = word_done ? checkFillIconImage : checkIconImage;
        const starImage = word_star ? starFillIconImage : starIconImage;

        const iconBox = `
                <div class="word-icons">
                <span id="${word_id}-star" class="panel-icon icon-btn-right" onclick="${starClickEvent}">
                  ${starImage}
                </span>
                <span id="${word_id}-done" class="panel-icon icon-btn-right" onclick="${doneClickEvent}">
                  ${doneImage}
                </span>
            </div>
        `;

        const textBox = `
            <div class="word-texts">
                <div class="word-span-box ${word_id}-span">
                    ${word_word}
                </div>
                <div class="word-span-box ${word_id}-span">
                    ${word_mean}
                </div>
                <div class="word-input-box ${word_id}-input" hidden>
                    <input id="${word_id}-word-edit" value="${word_word}">
                </div>
                <div class="word-input-box ${word_id}-input" hidden>
                    <input id="${word_id}-mean-edit" value="${word_mean}">
                </div>
            </div>
        `;

        const buttonBox = `
            <div class="word-buttons">
                <span class="panel-icon icon-btn-left ${word_id}-edit-icon" onclick="${editClickEvent}">
                    ${editButtonIconImage}
                </span>
                <span class="panel-icon icon-btn-left ${word_id}-remove-icon" onclick="${removeClickEvent}">
                    ${removeButtonIconImage}
                </span>
                <div class="panel-icon icon-btn-left ${word_id}-save-icon" style="display: none;" onclick="${saveClickEvent}">
                    ${saveButtonIconImage}
                </div>
                <span class="panel-icon icon-btn-left ${word_id}-cancel-icon" style="display: none;" onclick="${cancelClickEvent}">
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
}

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
        return {...state, isActive: i === index};
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
            const {ok, words, message} = res;

            if (!ok) return alert(message);
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

const wordStarClick = (word_id) => {
    const word_star = {word_star: }
    $.ajax({
        type: "POST",
        url: `/api/words/${word_id}`,
        data: {},
        success: (res) => {
            const {ok, message} = res;
            if (!ok) return alert(message);
        }
    })

    // Ajax 요청 결과
    const word = rows.find(word => word.word_id === word_id);
    const {word_star} = word;
    rows[rows.indexOf(word)] = {...word, word_star: !word_star}

    const span = $(`#${word_id}-star`);
    span.empty();
    span.append(!word_star ? starFillIconImage : starIconImage);
};

const wordDoneClick = (word_id) => {
    // Ajax 요청 결과
    const res = {ok: true};
    const {ok, message} = res;

    if (!ok) return alert(message);

    const word = rows.find(word => word.word_id === word_id);
    const {word_done} = word;
    rows[rows.indexOf(word)] = {...word, word_done: !word_done}

    const span = $(`#${word_id}-done`);
    span.empty();
    span.append(!word_done ? checkFillIconImage : checkIconImage);
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
    if (confirm("단어를 삭제하시겠습니까?")) {
        // Ajax 요청
        location.reload();
    }
};

const wordSaveClick = (word_id) => {
    const word_word = $(`#${word_id}-word-edit`).val();
    const word_mean = $(`#${word_id}-mean-edit`).val();

    if (!word_word) return alert("단어를 입력하세요.");
    if (!word_mean) return alert("뜻을 입력하세요.");

    const origin = rows.find(word => word.word_id === word_id);
    if (origin.word_word === word_word && origin.word_mean === word_mean) {
        return wordEditCancel(word_id);
    }

    // Ajax 요청
    alert("저장되었습니다.");
    // location.reload();
}

$(document).ready(() => {
    filterRender();
});
