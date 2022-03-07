# [항해99 Chapter #1] 1조 S.A(Starting Assignment)

## 1. 프로젝트 개요

- 프로젝트명 : Hello Word
- 내용 : 코딩도 중요하지만, 개발자의 문서는 대부분 영어로 되어 있기에 영어 공부도 빠뜨릴 수 없죠! 간단하게 어 단어를 암기할 수 있는 나만의 단어장입니다.

## 2. 와이어 프레임

- **로그인 페이지**

![1.png](images/1.PNG)

- **회원가입 페이지**

![2.png](images/2.png)

- **단어 리스트 페이지**

![3.png](images/3.png)

## 3. API

| 기능     | Method | URL                | request                                                      | response                                                     |
| -------- | ------ | ------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 로그인   | POST   | /api/login         | { id: String, passwd: String }                               | { ok: Boolean,  message?: String}                            |
| 회원가입 | POST   | /api/signup        | params = { id: String, name: String, passwd: String }        | { ok: Boolean,  message?: String}                            |
| 단어목록 | GET    | /api/words/:params | params = { done: Boolean, star: Boolean }                    | { rows: Array({ id: String, word: String, mean: String, done: Boolean, star: Boolean }) } |
| 단어추가 | POST   | /api/words         | { word: String, mean: String, done: Boolean, star: Boolean } | { ok: Boolean,  message?: String}                            |
| 단어수정 | PUT    | /api/words/:params | params = { id: String }<br>body = { done?: Boolean, star?: Boolean, word?: String, mean: String } | { ok: Boolean,  message?: String}                            |
| 단어삭제 | DELETE | /api/words/:params | params = { id: String }                                      | { ok: Boolean,  message?: String}                            |