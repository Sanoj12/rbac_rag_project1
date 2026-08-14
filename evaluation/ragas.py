
import json

from datasets import Dataset

from application.rag.retriever import retrieve_answer

from ragas import evaluate

from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
    ContextRecall
)


def ragas_evaluation():

    try:

        # --------------------------------------------------
        # 1. Load ground truth JSON
        # --------------------------------------------------

        with open(
            "evaluation/ground_truth.json",
            "r",
            encoding="utf-8"
        ) as f:

            ground_truth_data = json.load(f)


        # --------------------------------------------------
        # 2. Create empty lists
        # --------------------------------------------------

        questions = []
        answers = []
        contexts = []
        ground_truths = []


        # --------------------------------------------------
        # 3. Run your RAG system for every question
        # --------------------------------------------------

        for data in ground_truth_data:

            question = data.get("question", "")

            try:

                department = data["department"]

                expected_answer = data["ground_truth"]


                # Run your existing RAG pipeline
                answer, retrieved_contexts = retrieve_answer(
                    question,
                    department
                )


                # Save results
                questions.append(question)

                answers.append(answer)

                contexts.append(retrieved_contexts)

                ground_truths.append(expected_answer)


                print(f"Evaluation: {question}")


            except Exception as e:

                print(f"Failed question: {question}")
                print(f"Error: {e}")

                continue


        # --------------------------------------------------
        # 4. Check whether we have data
        # --------------------------------------------------

        if not questions:

            print("No questions were successfully evaluated.")

            return None


        # --------------------------------------------------
        # 5. Create HuggingFace Dataset
        # --------------------------------------------------

        dataset = Dataset.from_dict({

            "user_input": questions,

            "response": answers,

            "retrieved_contexts": contexts,

            "reference": ground_truths

        })


        print("\nDataset created successfully.")

        print("Number of questions:", len(questions))


        # --------------------------------------------------
        # 6. Define RAGAS metrics
        # --------------------------------------------------

        metrics = [

            Faithfulness(),

            AnswerRelevancy(),

            ContextPrecision(),

            ContextRecall()

        ]


        # --------------------------------------------------
        # 7. Run RAGAS evaluation
        # --------------------------------------------------

        results = evaluate(

            dataset=dataset,

            metrics=metrics

        )


        # --------------------------------------------------
        # 8. Convert result to pandas
        # --------------------------------------------------

        results_df = results.to_pandas()


        print("\nRAGAS Results:")
        print(results_df)


        # --------------------------------------------------
        # 9. Convert results to JSON
        # --------------------------------------------------

        results_json = results_df.to_dict(
            orient="records"
        )


        # --------------------------------------------------
        # 10. Save results
        # --------------------------------------------------

        with open(
            "evaluation/ragas_results.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                results_json,
                f,
                indent=4,
                ensure_ascii=False
            )


        print(
            "\nRAGAS evaluation completed successfully."
        )

        print(
            "Results saved to: "
            "evaluation/ragas_results.json"
        )


        return results_json


    except Exception as e:

        print("\nRAGAS evaluation failed.")

        print("Error:", e)

        return None


# --------------------------------------------------
# Run evaluation
# --------------------------------------------------

results = ragas_evaluation()