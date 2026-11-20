import random

class AIAgent:
    """
    A simple AI agent for quality control on a production line.
    It demonstrates operating within defined boundaries and explicitly
    recognizing when inputs are outside its operational scope.
    """

    def __init__(self, min_acceptable=70, max_acceptable=100):
        self.min_acceptable = min_acceptable
        self.max_acceptable = max_acceptable
        self.min_rework = 50 # Below this is rejected, above is reworkable
        self.min_reject = 0  # Absolute minimum for a valid score

    def inspect_product(self, quality_score):
        """
        Inspects a product based on its quality score.
        The agent explicitly identifies valid, problematic, and out-of-bounds inputs.
        """
        try:
            # Ensure the input is a number
            if not isinstance(quality_score, (int, float)):
                # This is where the agent 'knows its limits' by refusing to process
                # an invalid input type, signaling a need for human review.
                print(f"Agent: ERROR - Received non-numeric input '{quality_score}'. Cannot process.")
                return "STATUS: UNKNOWN_INPUT_TYPE - REQUIRES_HUMAN_REVIEW"

            # Check for physically impossible or out-of-sensor-range values.
            # This is another crucial 'knowing its limits' check: if data is beyond
            # any reasonable expectation, it's likely a system error, not a product issue.
            if quality_score < self.min_reject or quality_score > self.max_acceptable + 10: # +10 for a buffer
                print(f"Agent: WARNING - Quality score {quality_score} is outside expected sensor range [{self.min_reject}-{self.max_acceptable+10}].")
                return "STATUS: SENSOR_ERROR_OR_OUT_OF_BOUNDS - REQUIRES_HUMAN_REVIEW"

            # Process within defined operational boundaries
            if self.min_acceptable <= quality_score <= self.max_acceptable:
                print(f"Agent: Product quality score {quality_score} is within acceptable range.")
                return "STATUS: APPROVED"
            elif self.min_rework <= quality_score < self.min_acceptable:
                print(f"Agent: Product quality score {quality_score} is low, requires rework.")
                return "STATUS: NEEDS_REWORK"
            elif self.min_reject <= quality_score < self.min_rework:
                print(f"Agent: Product quality score {quality_score} is too low, product rejected.")
                return "STATUS: REJECTED"
            else:
                # This 'else' should ideally not be reached with comprehensive checks above,
                # but serves as a final fallback for an unforeseen internal state.
                # The agent acknowledges an unknown state, rather than making a bad decision.
                print(f"Agent: UNEXPECTED_STATE - Quality score {quality_score} did not match any known criteria.")
                return "STATUS: UNKNOWN_CRITERIA - REQUIRES_HUMAN_REVIEW"

        except Exception as e:
            # Catch any other unexpected errors during processing.
            # The agent explicitly reports critical processing failures.
            print(f"Agent: CRITICAL_ERROR - An unexpected error occurred: {e}. Cannot make decision.")
            return "STATUS: CRITICAL_PROCESSING_ERROR - REQUIRES_HUMAN_REVIEW"

if __name__ == "__main__":
    agent = AIAgent()

    print("--- Simulating product inspections ---")

    # Test cases demonstrating different scenarios
    test_scores = [
        95,  # Approved
        70,  # Approved (boundary)
        65,  # Needs rework
        50,  # Needs rework (boundary)
        30,  # Rejected
        0,   # Rejected (boundary)
        105, # Out of expected sensor range (e.g., sensor malfunction reading too high)
        -10, # Out of expected sensor range (e.g., sensor malfunction reading too low)
        "abc", # Invalid input type
        None,  # Invalid input type
        80.5, # Approved (float)
        random.uniform(70, 100) # Random approved
    ]

    for i, score in enumerate(test_scores):
        print(f"\nProduct {i+1} (Score: {score}):")
        result = agent.inspect_product(score)
        print(f"Decision: {result}")
