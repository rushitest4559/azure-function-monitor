import logging
import azure.functions as func
# from opentelemetry import metrics
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
# from azure.monitor.opentelemetry.exporter import AzureMonitorMetricExporter

app = func.FunctionApp()

# Configure OpenTelemetry provider + Azure Monitor exporter
# exporter = AzureMonitorMetricExporter()
# reader = PeriodicExportingMetricReader(exporter)
# provider = MeterProvider(metric_readers=[reader])
# metrics.set_meter_provider(provider)

# # Create a meter and counter
# meter = metrics.get_meter(__name__)
# discount_amount_counter = meter.create_counter(
#     "discount_amount",
#     description="Discount amount applied per request",
#     unit="₹",
# )

@app.route(route="discount", auth_level=func.AuthLevel.ANONYMOUS)
def discount(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Discount function started.")
    try:
        raw_amount = req.params.get("amount")
        if not raw_amount:
            logging.warning("Missing 'amount' parameter.")
            return func.HttpResponse("Missing amount parameter", status_code=400)

        amount = float(raw_amount)
        if amount <= 0:
            logging.warning(f"Invalid amount: {amount}")
            return func.HttpResponse("Invalid amount", status_code=400)

        discount_rate = 0.05
        discount_amount = amount * discount_rate
        final_price = amount - discount_amount

        # Log structured data (visible in traces/requests with customDimensions)
        logging.info(
            "Discount computed",
            extra={"custom_dimensions": {
                "original_amount": amount,
                "discount_amount": discount_amount,
                "final_price": final_price,
            }},
        )

        # Emit metric (visible in customMetrics table)
        # discount_amount_counter.add(discount_amount, {})

        return func.HttpResponse(
            f"Original: ${amount:.2f}, Discount: ${discount_amount:.2f}, Final: ${final_price:.2f}",
            status_code=200,
        )
    except ValueError:
        logging.error("Invalid amount format.")
        return func.HttpResponse("Invalid amount format", status_code=400)
    except Exception as e:
        logging.exception("Unexpected error: %s", e)
        return func.HttpResponse("Internal error", status_code=500)

@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Health check called.")
    return func.HttpResponse("Healthy", status_code=200)
