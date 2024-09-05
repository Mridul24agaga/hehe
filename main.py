import asyncio
from playwright.async_api import async_playwright

# Your Facebook credentials
FB_EMAIL = "aicognify@gmail.com"
FB_PASSWORD = "mridul24may"  # Replace with your actual password
FB_SECURITY_CODE = "240700"  # Security code for logging in

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Use headless=True for no GUI
        page = await browser.new_page()
        
        # Step 1: Open Facebook Login Page
        await page.goto('https://www.facebook.com/login')
        
        # Automatically fill in the email and password
        await page.fill("input[name='email']", FB_EMAIL)
        await page.fill("input[name='pass']", FB_PASSWORD)
        await page.press("input[name='pass']", 'Enter')  # Press Enter to log in
        
        # Wait for user to log in manually (if needed)
        await page.wait_for_timeout(5000)  # Adjust this timeout as needed
        print("Logged in successfully.")

        # Function to check messages and reply
        async def check_and_reply():
            await page.goto('https://www.facebook.com/messages')
            await page.wait_for_timeout(3000)  # Allow time for the page to load

            # Wait for the security code input to appear
            await page.wait_for_selector("input[type='text']", timeout=10000)  # Adjust timeout as needed
            print("Security code input detected. Waiting 4 seconds to enter the code...")
            await asyncio.sleep(4)  # Wait for 4 seconds before entering the security code

            # Automatically fill in the security code
            await page.fill("input[type='text']", FB_SECURITY_CODE)  # Fill in the security code
            await page.press("input[type='text']", 'Enter')  # Press Enter to continue

            await page.wait_for_timeout(3000)  # Allow time for the messages page to load

            # Select all conversation rows
            conversation_rows = await page.query_selector_all('//div[@role="row"]')

            for row in conversation_rows:
                # Click on the conversation to open it
                await row.click()
                await page.wait_for_timeout(2000)  # Allow time for the conversation to load

                # Select the message input box
                message_box = await page.query_selector("div[contenteditable='true']")
                
                # Get all messages in the conversation
                messages = await page.query_selector_all('//div[@role="row"]')

                # Get the last message text
                last_message = await messages[-1].inner_text() if messages else ""
                print("Last message received:", last_message)

                # Check if the last message is a new message (if it is not from you)
                if "You" not in last_message and last_message.strip() != "":
                    # Send the reply message
                    reply_message = (
                        "Hello, great news! It is currently available, and we're offering an exclusive move-in special: "
                        "choose between enjoying the last month of free rent or receiving half off the deposit. "
                        "For more details about the property and to apply, please click on the link below: "
                        "https://www.happyhome.casa/rentals.html. "
                        "Schedule a viewing using the following link: https://calendar.app.google/zTM3JDqmVkMoNNy48 "
                        "or contact us directly at 432-999-5677 via text or call. "
                        "We're looking forward to assisting you in finding your perfect home!"
                    )
                    await message_box.fill(reply_message)
                    await message_box.press('Enter')  # Press Enter to send the message
                    print("Sent auto-reply.")

                    # Wait for 10 seconds before sending the follow-up question
                    await page.wait_for_timeout(10000)

                    # Send the follow-up question
                    follow_up_question = "What city are you looking to rent in?"
                    await message_box.fill(follow_up_question)
                    await message_box.press('Enter')  # Send the follow-up question
                    print("Sent follow-up question.")
                    break  # Exit the loop after sending the follow-up question

        # Main loop to continuously check for messages
        try:
            while True:
                await check_and_reply()
                await asyncio.sleep(5)  # Wait before checking for new messages again
        except KeyboardInterrupt:
            print("Stopping the script...")
        finally:
            await browser.close()

# Run the async function
asyncio.run(run())
