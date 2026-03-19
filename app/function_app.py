import azure.functions as func
import logging
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.azure.metrics_exporter import new_metrics_exporter
from opencensus.stats import stats, measure, view, aggregation

app = func.FunctionApp()

# ----------------------------
# Telemetry Setup (Logs + Metrics)
# ----------------------------

# Configure logger for Application Insights (no explicit connection string needed)
logger = logging.getLogger("discount-function")
logger.addHandler(AzureLogHandler())  # Uses Function App's built-in AI link
logger.setLevel(logging.INFO)

# Stats recorder
stats_recorder = stats.stats_recorder

# Define a custom measure (metric)
measure_discount = measure.MeasureFloat(
    "discount_amount", "Amount of discount applied", "USD"
)

# Define a view (aggregation of the measure)
view_discount = view.View(
    "discount_amount_view",
    "Distribution of discount amounts",
    [measure_discount],
    aggregation.DistributionAggregation([0, 5, 10, 20, 50])  # buckets
)

# Register the view
stats.stats.view_manager.register_view(view_discount)

# Export metrics to Application Insights (no connection string needed)
exporter = new_metrics_exporter()
stats.stats.view_manager.register_exporter(exporter)

# ----------------------------
# Function Endpoints
# ----------------------------

@app.route(route="discount", auth_level=func.AuthLevel.ANONYMOUS)
def discount(req: func.HttpRequest) -> func.HttpResponse:
    try:
        amount_str = req.params.get('amount', None)
        if amount_str is None:
            logger.warning("Amount parameter missing in request")
            return func.HttpResponse("Missing 'amount' parameter", status_code=400)

        try:
            amount = float(amount_str)
        except ValueError:
            logger.error(f"Invalid amount value: {amount_str}", exc_info=True)
            return func.HttpResponse("Amount must be numeric", status_code=400)

        if amount <= 0:
            logger.info(f"Invalid amount received: {amount}")
            return func.HttpResponse("Invalid amount", status_code=400)

        discount_rate = 0.05  # 5% off
        discount_amount = amount * discount_rate
        final_price = amount - discount_amount

        # Custom telemetry for business events
        logger.info(
            f"DiscountApplied: original={amount}, discount={discount_amount}, final={final_price}"
        )

        # Record custom metric
        mmap = stats_recorder.new_measurement_map()
        mmap.measure_float_put(measure_discount, discount_amount)
        mmap.record()

        return func.HttpResponse(
            f"Original: ${amount:.2f}, Discount: ${discount_amount:.2f}, Final: ${final_price:.2f}",
            status_code=200
        )

    except Exception:
        logger.exception("Unexpected error in discount function")
        return func.HttpResponse("Internal Server Error", status_code=500)

# Health check endpoint for availability tests
@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse("Healthy", status_code=200)
