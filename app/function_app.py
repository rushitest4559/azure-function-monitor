import azure.functions as func

app = func.FunctionApp()

@app.route(route="discount", auth_level=func.AuthLevel.ANONYMOUS)
def discount(req: func.HttpRequest) -> func.HttpResponse:
    amount = float(req.params.get('amount', 0))
    if amount <= 0:
        return func.HttpResponse("Invalid amount", status_code=400)
    
    discount_rate = 0.05  # 5% off
    discount_amount = amount * discount_rate
    final_price = amount - discount_amount
    
    return func.HttpResponse(
        f"Original: ${amount:.2f}, Discount: ${discount_amount:.2f}, Final: ${final_price:.2f}",
        status_code=200
    )

@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        "Healthy",
        status_code=200
    )