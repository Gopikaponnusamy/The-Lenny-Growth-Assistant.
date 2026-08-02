import requests


# ==========================================
# OLLAMA CONFIGURATION
# ==========================================

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL_NAME = "llama3.2"


# ==========================================
# CHECK OLLAMA
# ==========================================

def check_ollama():

    try:

        response = requests.get(
            f"{OLLAMA_URL}/api/tags",
            timeout=10
        )

        if response.status_code != 200:

            return {
                "status": "error",
                "message": "Ollama is not responding."
            }

        data = response.json()

        models = []

        for model in data.get("models", []):

            models.append(
                model.get("name", "")
            )

        # Check whether our model exists

        model_exists = any(

            MODEL_NAME in model

            for model in models

        )

        if not model_exists:

            return {
                "status": "error",
                "message":
                    f"Model '{MODEL_NAME}' is not available.",
                "available_models":
                    models
            }

        return {

            "status": "ok",

            "model":
                MODEL_NAME

        }


    except requests.exceptions.ConnectionError:

        return {

            "status": "error",

            "message":
                "Could not connect to Ollama. "
                "Make sure Ollama is running."

        }


    except Exception as e:

        return {

            "status": "error",

            "message":
                str(e)

        }


# ==========================================
# GENERATE RESPONSE
# ==========================================

def generate_response(prompt):

    print("\n======================================")

    print("Sending prompt to Ollama...")

    print("Model:", MODEL_NAME)

    print("======================================\n")


    try:

        response = requests.post(

            f"{OLLAMA_URL}/api/generate",

            json={

                "model":
                    MODEL_NAME,

                "prompt":
                    prompt,

                "stream":
                    False,

                "options": {

                    "temperature":
                        0.3,

                    "num_ctx":
                        4096

                }

            },

            timeout=300

        )


        # Check HTTP error

        response.raise_for_status()


        # Convert response to JSON

        data = response.json()


        # Get generated answer

        answer = data.get(
            "response",
            ""
        )


        # Remove unnecessary spaces

        answer = answer.strip()


        if not answer:

            print(
                "WARNING: Ollama returned empty response."
            )


            return (
                "I could not generate an answer "
                "from the available transcript context."
            )


        print("\n======================================")

        print("OLLAMA RESPONSE RECEIVED")

        print("======================================")

        print(answer)

        print("======================================\n")


        return answer


    except requests.exceptions.ConnectionError:

        print(
            "ERROR: Cannot connect to Ollama."
        )


        return (

            "⚠️ Could not connect to Ollama. "

            "Please make sure Ollama is running."

        )


    except requests.exceptions.Timeout:

        print(

            "ERROR: Ollama request timed out."

        )


        return (

            "⚠️ Ollama took too long to respond. "

            "Please try again."

        )


    except requests.exceptions.HTTPError as e:

        print(

            "ERROR: Ollama HTTP error:",

            e

        )


        return (

            "⚠️ Ollama returned an HTTP error: "

            + str(e)

        )


    except Exception as e:

        print(

            "ERROR: Ollama error:",

            e

        )


        return (

            "⚠️ An error occurred while "

            "generating the response: "

            + str(e)

        )


# ==========================================
# ASK OLLAMA
# ==========================================

def ask_ollama(prompt):

    return generate_response(
        prompt
    )