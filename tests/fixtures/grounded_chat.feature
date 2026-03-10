Feature: Grounded chat
  Scenario: Answer from stored document
    Given a stored document titled "Grounding Guide" with content "Grounded systems cite evidence from retrieved knowledge."
    When the user asks "How do grounded systems answer?"
    Then the answer should contain grounded content
