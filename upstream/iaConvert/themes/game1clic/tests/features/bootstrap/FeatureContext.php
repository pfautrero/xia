<?php

use Behat\Behat\Context\ClosuredContextInterface,
    Behat\Behat\Context\TranslatedContextInterface,
    Behat\Behat\Context\BehatContext,
    Behat\Behat\Exception\PendingException;
use Behat\Gherkin\Node\PyStringNode,
    Behat\Gherkin\Node\TableNode;

use Behat\MinkExtension\Context\MinkContext;

//
// Require 3rd-party libraries here:
//
//   require_once 'PHPUnit/Autoload.php';
//   require_once 'PHPUnit/Framework/Assert/Functions.php';
//

/**
 * Features context.
 */
class FeatureContext extends MinkContext
{
    /**
     * Initializes context.
     * Every scenario gets it's own context object.
     *
     * @param array $parameters context parameters (set them up through behat.yml)
     */
    public function __construct(array $parameters)
    {
        // Initialize your context here
    }

//
// Place your definition and hook methods here:
//
//    /**
//     * @Given /^I have done something with "([^"]*)"$/
//     */
//    public function iHaveDoneSomethingWith($argument)
//    {
//        doSomethingWith($argument);
//    }
//


    /**
     * @When /^I click on Kinetic Object "([^"]*)"$/
     */
    public function iClickOnKineticObject($arg1)
    {
	$script = "
		for (var i in Kinetic.shapes) {\n
			if (Kinetic.shapes[i].attrs['name'] == '".str_replace("'", "\'", $arg1)."') {\n
				Kinetic.shapes[i].fire('click');\n
			}\n
		}";

        $this->getSession()->executeScript($script);
		$this->getSession()->wait(1000);
    }
}
