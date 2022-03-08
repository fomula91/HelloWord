let rows = [];
let filterState = [{
    item: "전체",
    isActive: false,
    query: {}
},{
    item: "즐겨찾기",
    isActive: false,
    query: {word_star: true}
},{
    item: "외운 단어",
    isActive: false,
    query: {word_done: true}
},{
    item: "아직 외우지 못한 단어",
    isActive: false,
    query: {word_done: false}
}]

const starIconImage = `<svg xmlns="http://www.w3.org/2000/svg"
width="16" height="16" fill="currentColor" class="bi bi-star" viewBox="0 0 16 16">
<path d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"/>
</svg>`;
const starFillIconImage = `<svg xmlns="http://www.w3.org/2000/svg"
width="16" height="16" fill="currentColor" class="bi bi-star-fill" viewBox="0 0 16 16">
<path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
</svg>`;
const checkIconImage = `<svg xmlns="http://www.w3.org/2000/svg"
width="16" height="16" fill="currentColor" class="bi bi-check-circle" viewBox="0 0 16 16">
<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
<path d="M10.97 4.97a.235.235 0 0 0-.02.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-1.071-1.05z"/>
</svg>`;
const checkFillIconImage = `<svg xmlns="http://www.w3.org/2000/svg"
width="16" height="16" fill="currentColor" class="bi bi-check-circle-fill" viewBox="0 0 16 16">
<path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
</svg>`;
const editButtonIconImage = `<svg xmlns="http://www.w3.org/2000/svg"
width="16" height="16" fill="currentColor" class="bi bi-pencil" viewBox="0 0 16 16">
<path d="M12.146.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1 0 .708l-10 10a.5.5 0 0 1-.168.11l-5 2a.5.5 0 0 1-.65-.65l2-5a.5.5 0 0 1 .11-.168l10-10zM11.207 2.5 13.5 4.793 14.793 3.5 12.5 1.207 11.207 2.5zm1.586 3L10.5 3.207 4 9.707V10h.5a.5.5 0 0 1 .5.5v.5h.5a.5.5 0 0 1 .5.5v.5h.293l6.5-6.5zm-9.761 5.175-.106.106-1.528 3.821 3.821-1.528.106-.106A.5.5 0 0 1 5 12.5V12h-.5a.5.5 0 0 1-.5-.5V11h-.5a.5.5 0 0 1-.468-.325z"/>
</svg>`;
const removeButtonIconImage = `<svg xmlns="http://www.w3.org/2000/svg"
width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
<path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
</svg>`;

const wordsRender = (words) => {
    const wordsBox = $('#words-box');
    wordsBox.empty();
    words.forEach((word, i) => {
        const {word_id, word_star, word_done, word_word, word_mean } = word;
        const wordClickEvent = `wordClick('${word_word}', '${word_mean}')`;
        const starClickEvent = `wordStarClick('${word_id}')`;
        const doneClickEvent = `wordDoneClick('${word_id}')`;
        const editClickEvent = `wordEditClick('${word_id}')`;
        const removeClickEvent = `wordRemoveClick('${word_id}')`;
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
                <div class="word-word" onclick="${wordClickEvent}">
                    ${word_word}
                </div>
                <div class="word-mean" onclick="${wordClickEvent}">
                    ${word_mean}
                </div>
            </div>
        `;

        const buttonBox = `
            <div class="word-buttons">
                <span class="panel-icon icon-btn-left" onclick="${editClickEvent}">
                  ${editButtonIconImage}
                </span>
                <span class="panel-icon icon-btn-left" onclick="${removeClickEvent}">
                  ${removeButtonIconImage}
                </span>
            </div>
        `;

        const p = `
              <div class="panel-block is-active">
                ${iconBox}
                ${textBox}
                ${buttonBox}
              </div>`;
        wordsBox.append(p);
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
    console.log(`/api/words${query}`);
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
    // Ajax 요청 결과
    const res = {ok: true};
    const {ok, message} = res;

    if (!ok) return alert(message);

    const word = rows.find(word => word.word_id === word_id);
    const {word_star} = word;
    rows[rows.indexOf(word)] = {...word, word_star: !word_star}

    const span = $(`#${word_id}-star`);
    span.empty();
    span.append(!word_star ? starFillIconImage : starIconImage);
};

const wordDoneClick = (word_id) => {
    // Ajax 요청 결과
    console.log(word_id);
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

const wordClick = (word_word, word_mean) => {
    const content = `
        <p>${word_word}</p>
        <p>${word_mean}</p>
    `;
    $('#word-modal-content').append(content);
    $('#word-modal').show();
};

const wordEditClick = (word_id) => {
    const word = rows.find(word => word.word_id === word_id);
    const {word_word, word_mean} = word;

    const wordEditCompleteEvent = `wordEditComplete('${word_id}')`;
    const wordEditCancelEvent = `wordEditCancel()`;

    const content = `
        <input id="word-new-word" value="${word_word}" >
        <input id="word-new-mean" value="${word_mean}" >
        <button onclick="${wordEditCompleteEvent}">수정</button>
        <button onclick="${wordEditCancelEvent}">취소</button>
    `;
    $('#word-modal-content').append(content);
    $('#word-modal').show();
};

const wordRemoveClick = (word_id) => {
    if (confirm("단어를 삭제하시겠습니까?")) {
        // Ajax 요청
        location.reload();
    }
};

const modalClose = () => {
    $('#word-modal-content').empty();
    $('#word-modal').hide();
};

const wordEditComplete = () => {
    const newWord = $("#word-new-word").val();
    const newMean = $("#word-new-mean").val();

    if (newWord === "") return alert("단어를 입력하세요.");
    if (newMean === "") return alert("단어의 뜻을 입력하세요.");

    // Ajax 요청 -> 새로고침
    location.reload();
};

const wordEditCancel = () => {
    $('#word-modal-content').empty();
    $('#word-modal').hide();
};

$(document).ready(() => {
    filterRender();
});