Feature: test
  In order to test XIA
  As normal user
  I need to see something

  @javascript
  Scenario: check title
    Given I am on "index.html"
    Then I should see "Les gentils animaux de l'école"
    And I should not see "Le gentil éléphant de la savane"

  @javascript
  Scenario: check click on drop down menu
    Given I am on "index.html"
    When I follow "L'éléphant"
    Then I should see "Le gentil éléphant de la savane"
    And I should not see "Pour commencer, une petite vidéo :"

  @javascript
  Scenario: check click on canvas element
    Given I am on "index.html"
    When I click on Kinetic Object "L'éléphant"
    Then I should see "Le gentil éléphant de la savane"
