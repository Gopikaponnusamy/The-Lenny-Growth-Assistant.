// ==========================================
// LENNY GROWTH ASSISTANT - FRONTEND
// ==========================================

// Backend URL
const API_BASE = "http://127.0.0.1:8000";


// ==========================================
// GLOBAL VARIABLES
// ==========================================

let currentSessionId = null;
let allSessions = [];


// ==========================================
// PAGE LOAD
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    console.log("Lenny Growth Assistant loaded");

    loadSessions();

    setupTextarea();

});


// ==========================================
// LOAD ALL CHAT SESSIONS
// ==========================================

async function loadSessions() {

    try {

        const response = await fetch(
            `${API_BASE}/api/sessions`
        );

        if (!response.ok) {

            throw new Error(
                "Could not load sessions"
            );

        }

        allSessions = await response.json();

        renderChatHistory();

    } catch (error) {

        console.error(
            "Error loading sessions:",
            error
        );

    }

}


// ==========================================
// RENDER CHAT HISTORY
// ==========================================

function renderChatHistory(
    sessions = allSessions
) {

    const history =
        document.getElementById(
            "chatHistory"
        );

    if (!history) {

        return;

    }


    history.innerHTML = "";


    if (
        !sessions ||
        sessions.length === 0
    ) {

        history.innerHTML = `

            <div
                style="
                    color:#777;
                    font-size:12px;
                    padding:15px 10px;
                    text-align:center;
                "
            >
                No conversations yet
            </div>

        `;

        return;

    }


    sessions.forEach(
        session => {

            const item =
                document.createElement(
                    "div"
                );

            item.className =
                "chat-item";


            if (
                session.id ===
                currentSessionId
            ) {

                item.classList.add(
                    "active"
                );

            }


            const title =
                document.createElement(
                    "span"
                );

            title.textContent =
                session.title ||
                "New Chat";


            item.appendChild(
                title
            );


            item.onclick =
                function () {

                    openChat(
                        session.id
                    );

                };


            history.appendChild(
                item
            );

        }
    );

}


// ==========================================
// CREATE NEW CHAT
// ==========================================

async function createNewChat() {

    try {

        const response =
            await fetch(
                `${API_BASE}/api/sessions`,
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        title:
                            "New Chat"

                    })

                }
            );


        if (!response.ok) {

            throw new Error(
                "Could not create chat"
            );

        }


        const session =
            await response.json();


        console.log(
            "New session created:",
            session
        );


        currentSessionId =
            session.id;


        // Clear chat

        clearMessages();


        // Show welcome

        showWelcome();


        // Reload history

        await loadSessions();


        // Mobile sidebar close

        closeMobileSidebar();


    } catch (error) {

        console.error(
            "Create chat error:",
            error
        );


        alert(
            "Could not create a new chat. Please make sure the backend is running."
        );

    }

}


// ==========================================
// OPEN EXISTING CHAT
// ==========================================

async function openChat(
    sessionId
) {

    try {

        currentSessionId =
            sessionId;


        clearMessages();


        hideWelcome();


        const response =
            await fetch(

                `${API_BASE}/api/sessions/${sessionId}`

            );


        if (!response.ok) {

            throw new Error(
                "Could not load chat"
            );

        }


        const session =
            await response.json();


        console.log(
            "Opened session:",
            session
        );


        // ----------------------------------
        // HANDLE DIFFERENT RESPONSE FORMATS
        // ----------------------------------

        let messages =
            session.messages ||
            session.history ||
            [];


        if (
            Array.isArray(
                messages
            )
        ) {

            messages.forEach(
                message => {

                    const role =
                        message.role ||
                        message.sender ||
                        "assistant";


                    const content =
                        message.content ||
                        message.message ||
                        "";


                    if (
                        content
                    ) {

                        addMessage(

                            role === "user"
                                ? "user"
                                : "assistant",

                            content

                        );

                    }

                }
            );

        }


        renderChatHistory();


        closeMobileSidebar();


    } catch (error) {

        console.error(
            "Open chat error:",
            error
        );


        alert(
            "Could not open this chat."
        );

    }

}


// ==========================================
// SEND MESSAGE
// ==========================================

async function sendMessage() {

    const input =
        document.getElementById(
            "messageInput"
        );

    const sendButton =
        document.getElementById(
            "sendButton"
        );


    if (!input) {

        return;

    }


    const message =
        input.value.trim();


    if (!message) {

        return;

    }


    // --------------------------------------
    // CREATE SESSION IF NEEDED
    // --------------------------------------

    if (
        !currentSessionId
    ) {

        try {

            const response =
                await fetch(
                    `${API_BASE}/api/sessions`,
                    {

                        method: "POST",

                        headers: {

                            "Content-Type":
                                "application/json"

                        },

                        body:
                            JSON.stringify({

                                title:
                                    message.substring(
                                        0,
                                        50
                                    )

                            })

                        }
                );


            if (!response.ok) {

                throw new Error(
                    "Session creation failed"
                );

            }


            const session =
                await response.json();


            currentSessionId =
                session.id;


            await loadSessions();


        } catch (error) {

            console.error(
                "Session error:",
                error
            );


            alert(
                "Could not create a chat session."
            );


            return;

        }

    }


    // --------------------------------------
    // SHOW USER MESSAGE
    // --------------------------------------

    addMessage(
        "user",
        message
    );


    // Clear input

    input.value = "";


    autoResizeTextarea();


    // Hide welcome

    hideWelcome();


    // Disable button

    if (sendButton) {

        sendButton.disabled =
            true;

    }


    // Show typing

    showTyping();


    try {

        console.log(
            "Sending message:",
            message
        );


        const response =
            await fetch(

                `${API_BASE}/api/sessions/${currentSessionId}/messages`,

                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json",

                        "Accept":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            content:
                                message

                        })

                }

            );


        console.log(
            "Response status:",
            response.status
        );


        if (!response.ok) {

            const errorText =
                await response.text();


            console.error(
                "Backend error:",
                errorText
            );


            throw new Error(
                `Server error: ${response.status}`
            );

        }


        const data =
            await response.json();


        console.log(
            "Backend response:",
            data
        );


        hideTyping();


        // ----------------------------------
        // GET ANSWER
        // ----------------------------------

        let answer =
            data.content ||
            data.response ||
            data.answer ||
            data.message ||
            "";


        // ----------------------------------
        // FALLBACK
        // ----------------------------------

        if (
            typeof answer ===
            "object"
        ) {

            answer =
                answer.content ||
                JSON.stringify(
                    answer
                );

        }


        if (
            !answer ||
            answer.trim() === ""
        ) {

            answer =
                "Sorry, I could not generate an answer.";

        }


        // ----------------------------------
        // ADD ASSISTANT ANSWER
        // ----------------------------------

        addMessage(
            "assistant",
            answer
        );


        // ----------------------------------
        // ARTIFACT
        // ----------------------------------

        if (
            data.artifact
        ) {

            showArtifact(
                data.artifact
            );

        }


        // Reload chats

        await loadSessions();


    } catch (error) {

        console.error(
            "Send message error:",
            error
        );


        hideTyping();


        addMessage(

            "assistant",

            "⚠️ I could not generate an answer. Please check that the FastAPI backend and Ollama are running."

        );

    } finally {

        if (sendButton) {

            sendButton.disabled =
                false;

        }

    }

}


// ==========================================
// ADD MESSAGE TO CHAT
// ==========================================

function addMessage(
    role,
    content
) {

    const messages =
        document.getElementById(
            "messages"
        );


    if (!messages) {

        return;

    }


    hideWelcome();


    // --------------------------------------
    // USER MESSAGE
    // --------------------------------------

    if (
        role === "user"
    ) {

        const userMessage =
            document.createElement(
                "div"
            );


        userMessage.className =
            "user-message";


        userMessage.textContent =
            content;


        messages.appendChild(
            userMessage
        );


    }

    // --------------------------------------
    // ASSISTANT MESSAGE
    // --------------------------------------

    else {

        const assistantMessage =
            document.createElement(
                "div"
            );


        assistantMessage.className =
            "assistant-message";


        const avatar =
            document.createElement(
                "div"
            );


        avatar.className =
            "message-avatar assistant-avatar";


        avatar.textContent =
            "L";


        const messageContent =
            document.createElement(
                "div"
            );


        messageContent.className =
            "message-content";


        // Markdown support

        if (
            typeof marked !==
            "undefined"
        ) {

            messageContent.innerHTML =
                marked.parse(
                    content
                );

        } else {

            messageContent.textContent =
                content;

        }


        // Copy button

        const actions =
            document.createElement(
                "div"
            );


        actions.style.marginTop =
            "10px";


        const copyButton =
            document.createElement(
                "button"
            );


        copyButton.textContent =
            "Copy";


        copyButton.style.cssText = `

            border: 1px solid #ddd;
            background: white;
            border-radius: 6px;
            padding: 5px 10px;
            font-size: 11px;
            cursor: pointer;
            color: #666;

        `;


        copyButton.onclick =
            async function () {

                try {

                    await navigator.clipboard.writeText(
                        content
                    );


                    copyButton.textContent =
                        "Copied!";


                    setTimeout(
                        function () {

                            copyButton.textContent =
                                "Copy";

                        },
                        1500
                    );


                } catch (error) {

                    console.error(
                        "Copy error:",
                        error
                    );

                }

            };


        actions.appendChild(
            copyButton
        );


        messageContent.appendChild(
            actions
        );


        assistantMessage.appendChild(
            avatar
        );


        assistantMessage.appendChild(
            messageContent
        );


        messages.appendChild(
            assistantMessage
        );

    }


    // Scroll down

    setTimeout(
        scrollToBottom,
        50
    );

}


// ==========================================
// USE SUGGESTION
// ==========================================

function useSuggestion(
    button
) {

    if (!button) {

        return;

    }


    const text =
        button.querySelector(
            ".suggestion-content span"
        );


    let question = "";


    if (text) {

        question =
            text.textContent.trim();

    } else {

        question =
            button.textContent.trim();

    }


    const input =
        document.getElementById(
            "messageInput"
        );


    if (input) {

        input.value =
            question;


        autoResizeTextarea();


        input.focus();


        // Automatically send

        sendMessage();

    }

}


// ==========================================
// SHOW WELCOME
// ==========================================

function showWelcome() {

    const welcome =
        document.getElementById(
            "welcomeScreen"
        );


    if (welcome) {

        welcome.style.display =
            "block";

    }

}


// ==========================================
// HIDE WELCOME
// ==========================================

function hideWelcome() {

    const welcome =
        document.getElementById(
            "welcomeScreen"
        );


    if (welcome) {

        welcome.style.display =
            "none";

    }

}


// ==========================================
// CLEAR MESSAGES
// ==========================================

function clearMessages() {

    const messages =
        document.getElementById(
            "messages"
        );


    if (messages) {

        messages.innerHTML =
            "";

    }

}


// ==========================================
// TYPING INDICATOR
// ==========================================

function showTyping() {

    const typing =
        document.getElementById(
            "typingIndicator"
        );


    if (typing) {

        typing.classList.remove(
            "hidden"
        );

    }


    scrollToBottom();

}


function hideTyping() {

    const typing =
        document.getElementById(
            "typingIndicator"
        );


    if (typing) {

        typing.classList.add(
            "hidden"
        );

    }

}


// ==========================================
// SCROLL TO BOTTOM
// ==========================================

function scrollToBottom() {

    const messages =
        document.getElementById(
            "messages"
        );


    if (messages) {

        messages.scrollTop =
            messages.scrollHeight;

    }

}


// ==========================================
// TEXTAREA
// ==========================================

function setupTextarea() {

    const input =
        document.getElementById(
            "messageInput"
        );


    if (!input) {

        return;

    }


    input.addEventListener(
        "input",
        autoResizeTextarea
    );

}


function autoResizeTextarea() {

    const input =
        document.getElementById(
            "messageInput"
        );


    if (!input) {

        return;

    }


    input.style.height =
        "auto";


    input.style.height =
        Math.min(

            input.scrollHeight,

            150

        ) + "px";

}


// ==========================================
// ENTER KEY
// ==========================================

function handleKeyDown(
    event
) {

    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {

        event.preventDefault();

        sendMessage();

    }

}


// ==========================================
// SEARCH CHATS
// ==========================================

function searchChats() {

    const input =
        document.getElementById(
            "searchChats"
        );


    if (!input) {

        return;

    }


    const query =
        input.value
            .toLowerCase()
            .trim();


    if (!query) {

        renderChatHistory(
            allSessions
        );

        return;

    }


    const filtered =
        allSessions.filter(
            session =>

                (
                    session.title ||
                    "New Chat"
                )
                .toLowerCase()
                .includes(
                    query
                )

        );


    renderChatHistory(
        filtered
    );

}


// ==========================================
// SIDEBAR TOGGLE
// ==========================================

function toggleSidebar() {

    const sidebar =
        document.getElementById(
            "sidebar"
        );


    const overlay =
        document.getElementById(
            "sidebarOverlay"
        );


    if (!sidebar) {

        return;

    }


    sidebar.classList.toggle(
        "open"
    );


    if (overlay) {

        overlay.classList.toggle(
            "active"
        );

    }

}


function closeMobileSidebar() {

    const sidebar =
        document.getElementById(
            "sidebar"
        );


    const overlay =
        document.getElementById(
            "sidebarOverlay"
        );


    if (sidebar) {

        sidebar.classList.remove(
            "open"
        );

    }


    if (overlay) {

        overlay.classList.remove(
            "active"
        );

    }

}


// ==========================================
// ARTIFACT
// ==========================================

function showArtifact(
    artifact
) {

    const panel =
        document.getElementById(
            "artifactPanel"
        );


    if (!panel) {

        return;

    }


    panel.classList.remove(
        "hidden"
    );


    const title =
        document.getElementById(
            "artifactTitle"
        );


    const preview =
        document.getElementById(
            "artifactPreview"
        );


    const code =
        document.getElementById(
            "artifactCode"
        );


    if (
        title &&
        artifact.title
    ) {

        title.textContent =
            artifact.title;

    }


    if (
        preview
    ) {

        preview.innerHTML =
            artifact.content ||
            artifact.preview ||
            "";

    }


    if (
        code
    ) {

        code.textContent =
            artifact.code ||
            "";

    }

}


function closeArtifact() {

    const panel =
        document.getElementById(
            "artifactPanel"
        );


    if (panel) {

        panel.classList.add(
            "hidden"
        );

    }

}


function showArtifactPreview() {

    const preview =
        document.getElementById(
            "artifactPreview"
        );


    const code =
        document.getElementById(
            "artifactCode"
        );


    const previewTab =
        document.getElementById(
            "previewTab"
        );


    const codeTab =
        document.getElementById(
            "codeTab"
        );


    if (preview) {

        preview.classList.remove(
            "hidden"
        );

    }


    if (code) {

        code.classList.add(
            "hidden"
        );

    }


    if (previewTab) {

        previewTab.classList.add(
            "active"
        );

    }


    if (codeTab) {

        codeTab.classList.remove(
            "active"
        );

    }

}


function showArtifactCode() {

    const preview =
        document.getElementById(
            "artifactPreview"
        );


    const code =
        document.getElementById(
            "artifactCode"
        );


    const previewTab =
        document.getElementById(
            "previewTab"
        );


    const codeTab =
        document.getElementById(
            "codeTab"
        );


    if (preview) {

        preview.classList.add(
            "hidden"
        );

    }


    if (code) {

        code.classList.remove(
            "hidden"
        );

    }


    if (previewTab) {

        previewTab.classList.remove(
            "active"
        );

    }


    if (codeTab) {

        codeTab.classList.add(
            "active"
        );

    }

}