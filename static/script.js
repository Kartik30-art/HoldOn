"use strict";

const form = document.getElementById("analyze-form");
const messageInput = document.getElementById("message-input");
const charCount = document.getElementById("char-count");
const clearButton = document.getElementById("clear-button");
const analyzeButton = document.getElementById("analyze-button");
const buttonText = document.getElementById("button-text");
const buttonIcon = document.getElementById("button-icon");

const results = document.getElementById("results");
const riskBadge = document.getElementById("risk-badge");
const resultMessage = document.getElementById("result-message");
const riskValue = document.getElementById("risk-value");
const warningCount = document.getElementById("warning-count");
const warningList = document.getElementById("warning-list");
const nextSteps = document.getElementById("next-steps");

const connectionLabel = document.getElementById("connection-label");
const detectionStatus = document.getElementById("detection-status");
const adviceStatus = document.getElementById("advice-status");
const detectionTool = document.getElementById("tool-detection");
const adviceTool = document.getElementById("tool-advice");

const mlPrediction = document.getElementById("ml-prediction");
const mlScore = document.getElementById("ml-score");
const mlDisclaimer = document.getElementById("ml-disclaimer");

function updateCharacterCount() {
    if (!messageInput || !charCount) return;
    charCount.textContent = `${messageInput.value.length} / 10000 characters`;
}

function setToolStatus(tool, statusElement, status, text) {
    if (tool) {
        tool.classList.remove("is-running", "is-success", "is-error");
        if (status) tool.classList.add(`is-${status}`);
    }

    if (statusElement) statusElement.textContent = text;
}

function resetToolStatuses() {
    setToolStatus(detectionTool, detectionStatus, "", "Waiting");
    setToolStatus(adviceTool, adviceStatus, "", "Waiting");

    if (connectionLabel) connectionLabel.textContent = "Ready for a message";
}

function setRunningState(isRunning) {
    if (analyzeButton) analyzeButton.disabled = isRunning;
    if (messageInput) messageInput.disabled = isRunning;
    if (clearButton) clearButton.disabled = isRunning;

    if (buttonText) {
        buttonText.textContent = isRunning
            ? "Checking message..."
            : "Check this message";
    }

    if (buttonIcon) buttonIcon.textContent = isRunning ? "…" : "⌕";
}

function renderMLAnalysis(ml) {
    if (mlPrediction) mlPrediction.replaceChildren();
    if (mlScore) mlScore.textContent = "";

    if (!ml || ml.available === false) {
        if (mlPrediction) {
            mlPrediction.textContent = "ML prediction unavailable";
        }

        if (mlScore) {
            mlScore.textContent =
                ml?.message || "The rule-based analysis is still available.";
        }

        if (mlDisclaimer) {
            mlDisclaimer.textContent =
                "The experimental model could not provide a prediction. " +
                "Use the warning signs and safety advice above.";
        }

        return;
    }

    const prediction = String(ml.prediction || "unknown").toLowerCase();

    if (mlPrediction) {
        const label = document.createElement("strong");

        if (prediction === "scam") {
            label.textContent = "Model prediction: Potential scam";
        } else if (prediction === "legitimate") {
            label.textContent = "Model prediction: Likely legitimate";
        } else {
            label.textContent = `Model prediction: ${prediction}`;
        }

        mlPrediction.appendChild(label);
    }

    if (mlScore) {
        if (
            typeof ml.confidence === "number" &&
            Number.isFinite(ml.confidence)
        ) {
            mlScore.textContent =
                `Model score: ${(ml.confidence * 100).toFixed(2)}%`;
        } else {
            mlScore.textContent = "Model score unavailable.";
        }
    }

    if (mlDisclaimer) {
        mlDisclaimer.textContent =
            "Experimental TF-IDF + Logistic Regression model, trained on " +
            "only 20 sample messages. This score is not calibrated, verified " +
            "accuracy, or proof that a message is safe or fraudulent.";
    }
}

function showError(message) {
    if (results) results.hidden = false;

    if (riskBadge) {
        riskBadge.className = "risk-badge";
        riskBadge.textContent = "Unavailable";
    }

    if (resultMessage) resultMessage.textContent = message;
    if (riskValue) riskValue.textContent = "—";
    if (warningCount) warningCount.textContent = "—";

    if (warningList) {
        warningList.replaceChildren();

        const item = document.createElement("div");
        item.className = "warning-item";

        const heading = document.createElement("strong");
        heading.textContent = "Analysis could not be completed";

        const detail = document.createElement("span");
        detail.textContent =
            "Check the website and MCP server terminals, then try again.";

        item.append(heading, detail);
        warningList.appendChild(item);
    }

    if (nextSteps) {
        nextSteps.replaceChildren();

        const step = document.createElement("li");
        step.textContent =
            "Do not act on a suspicious message until you verify it independently.";

        nextSteps.appendChild(step);
    }

    renderMLAnalysis(null);
}

function renderResults(data) {
    if (results) results.hidden = false;

    const risk = String(data.risk_level || "unknown").toLowerCase();

    if (riskBadge) {
        riskBadge.className = "risk-badge";

        if (["high", "medium", "low"].includes(risk)) {
            riskBadge.classList.add(risk);
        }

        riskBadge.textContent = `${risk} risk`;
    }

    if (riskValue) riskValue.textContent = risk;
    if (resultMessage) resultMessage.textContent = data.message || "Analysis completed.";

    // Use the actual warning array so the count matches the displayed entries.
    const warnings = Array.isArray(data.warning_signs)
        ? data.warning_signs
        : [];

    if (warningCount) {
        warningCount.textContent = String(warnings.length);
    }

    if (warningList) {
        warningList.replaceChildren();

        if (warnings.length === 0) {
            const item = document.createElement("div");
            item.className = "warning-item";

            const heading = document.createElement("strong");
            heading.textContent = "No listed warning signs found";

            const detail = document.createElement("span");
            detail.textContent =
                "This does not guarantee the message is safe.";

            item.append(heading, detail);
            warningList.appendChild(item);
        } else {
            warnings.forEach((warning) => {
                const item = document.createElement("div");
                item.className = "warning-item";

                const heading = document.createElement("strong");
                heading.textContent = String(warning.category || "Warning")
                    .replaceAll("_", " ")
                    .replace(/\b\w/g, letter => letter.toUpperCase());

                const detail = document.createElement("span");
                detail.textContent = String(warning.evidence || "");

                item.append(heading, detail);
                warningList.appendChild(item);
            });
        }
    }

    if (nextSteps) {
        nextSteps.replaceChildren();

        const steps = Array.isArray(data.next_steps)
            ? data.next_steps
            : [];

        if (steps.length > 0) {
            steps.forEach((text) => {
                const item = document.createElement("li");
                item.textContent = String(text);
                nextSteps.appendChild(item);
            });
        } else {
            const item = document.createElement("li");
            item.textContent =
                "Verify the sender independently before taking action.";
            nextSteps.appendChild(item);
        }
    }

    renderMLAnalysis(data.ml_analysis);

    if (results) {
        results.scrollIntoView({
            behavior: "smooth",
            block: "start"
        });
    }
}

if (messageInput) {
    messageInput.addEventListener("input", updateCharacterCount);
}

if (clearButton) {
    clearButton.addEventListener("click", () => {
        if (messageInput) {
            messageInput.value = "";
            updateCharacterCount();
            messageInput.focus();
        }

        if (results) results.hidden = true;

        renderMLAnalysis(null);
        resetToolStatuses();
    });
}

document.querySelectorAll(".example-button").forEach((button) => {
    button.addEventListener("click", () => {
        if (!messageInput) return;

        messageInput.value = button.dataset.example || "";
        updateCharacterCount();
        messageInput.focus();
    });
});

if (form) {
    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const message = messageInput ? messageInput.value.trim() : "";

        if (!message) {
            if (messageInput) messageInput.focus();
            return;
        }

        if (results) results.hidden = true;

        resetToolStatuses();
        setRunningState(true);

        if (connectionLabel) {
            connectionLabel.textContent = "Contacting HoldOn MCP server";
        }

        setToolStatus(
            detectionTool, detectionStatus, "running", "Request in progress"
        );

        setToolStatus(
            adviceTool, adviceStatus, "running", "Request in progress"
        );

        try {
            const response = await fetch("/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message })
            });

            let data;

            try {
                data = await response.json();
            } catch {
                throw new Error(
                    "The server returned an unreadable response. " +
                    "Check the website terminal."
                );
            }

            if (!response.ok) {
                throw new Error(
                    data.detail ||
                    data.error ||
                    `The analysis request failed (HTTP ${response.status}).`
                );
            }

            if (data.error) throw new Error(data.error);

            renderResults(data);

            setToolStatus(
                detectionTool, detectionStatus, "success",
                "Analysis response received"
            );

            setToolStatus(
                adviceTool, adviceStatus, "success",
                "Safety advice received"
            );

            if (connectionLabel) {
                connectionLabel.textContent = "Analysis completed successfully";
            }
        } catch (error) {
            console.error("HoldOn analysis error:", error);

            setToolStatus(
                detectionTool, detectionStatus, "error",
                "Request failed or unavailable"
            );

            setToolStatus(
                adviceTool, adviceStatus, "error",
                "Result not confirmed"
            );

            if (connectionLabel) {
                connectionLabel.textContent = "Analysis unavailable";
            }

            showError(
                error.message ||
                "Could not analyze this message. Please try again."
            );
        } finally {
            setRunningState(false);
        }
    });
}

updateCharacterCount();
resetToolStatuses();
renderMLAnalysis(null);