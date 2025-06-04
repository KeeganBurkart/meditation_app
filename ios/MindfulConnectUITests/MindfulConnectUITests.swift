import XCTest

final class MindfulConnectUITests: XCTestCase {
    private var app: XCUIApplication!

    override func setUp() {
        continueAfterFailure = false
        app = XCUIApplication()
        app.launch()
    }

    func testStartTimerAndFinish() {
        let startButton = app.buttons["Start"]
        XCTAssertTrue(startButton.exists, "Start button should be present")
        startButton.tap()

        // Wait for a label that indicates the timer finished
        let finishedLabel = app.staticTexts["Finished"]
        let expectation = XCTNSPredicateExpectation(predicate: NSPredicate(format: "exists == true"), object: finishedLabel)
        let result = XCTWaiter().wait(for: [expectation], timeout: 10)
        XCTAssertEqual(result, .completed, "Timer should complete and display Finished label")
    }
}
