import logging
import azure.functions as func


app = func.FunctionApp()


@app.route(route="discount", auth_level=func.AuthLevel.ANONYMOUS)
def discount(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Discount function started.")

    try:
        raw_amount = req.params.get("amount")
        if not raw_amount:
            logging.warning("Missing 'amount' parameter.")
            return func.HttpResponse(
                "Missing amount parameter",
                status_code=400,
            )

        amount = float(raw_amount)
        if amount <= 0:
            logging.warning(f"Invalid amount: {amount}")
            return func.HttpResponse(
                "Invalid amount",
                status_code=400,
            )

        discount_rate = 0.05  # 5% off
        discount_amount = amount * discount_rate
        final_price = amount - discount_amount

        # Log structured data (custom_dimensions will appear in App Insights)
        logging.info(
            "Discount computed",
            extra={
                "custom_dimensions": {
                    "original_amount": amount,
                    "discount_amount": discount_amount,
                    "final_price": final_price,
                }
            },
        )

        # To see discount_amount in KQL:
        #   traces
        #   | where message has "Discount computed"
        #   | extend amount_d = tostring(customDimensions.discount_amount)

        return func.HttpResponse(
            f"Original: ${amount:.2f}, "
            f"Discount: ${discount_amount:.2f}, "
            f"Final: ${final_price:.2f}",
            status_code=200,
        )

    except ValueError as e:
        logging.error("Invalid amount format: %s", e)
        return func.HttpResponse(
            "Invalid amount format",
            status_code=400,
        )

    except Exception as e:
        logging.exception("Unexpected error in discount function: %s", e)
        return func.HttpResponse(
            "Internal error",
            status_code=500,
        )


@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Health check called.")
    return func.HttpResponse(
        "Healthy",
        status_code=200,
    )
