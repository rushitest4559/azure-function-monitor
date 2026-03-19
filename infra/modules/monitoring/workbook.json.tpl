{
  "version": "Notebook/1.0",
  "items": [
    {
      "type": 1,
      "content": {
        "json": "## 📊 Azure Function: Discount Monitoring\nThis dashboard shows live telemetry from the Discount Function, including requests, failures, and custom discount metrics."
      }
    },
    {
      "type": 3,
      "content": {
        "version": "KqlParameterItem/1.0",
        "query": "requests | summarize Count=count() by Result=iff(success==true, 'Success', 'Failed')",
        "size": 1,
        "title": "Total Requests (Last 24h)",
        "queryType": 0,
        "resourceType": "microsoft.insights/components",
        "visualization": "tiles",
        "tileSettings": {
          "showBadge": true,
          "titleConfig": { "columnId": "Result" },
          "leftConfig": { "columnId": "Count" }
        }
      }
    },
    {
      "type": 3,
      "content": {
        "version": "KqlParameterItem/1.0",
        "query": "requests | summarize avg(duration) by bin(timestamp, 1h)",
        "title": "Average Request Duration (ms)",
        "queryType": 0,
        "resourceType": "microsoft.insights/components",
        "visualization": "timechart"
      }
    },
    {
      "type": 3,
      "content": {
        "version": "KqlParameterItem/1.0",
        "query": "exceptions | summarize Count=count() by type",
        "title": "Exceptions by Type",
        "queryType": 0,
        "resourceType": "microsoft.insights/components",
        "visualization": "barchart"
      }
    },
    {
      "type": 3,
      "content": {
        "version": "KqlParameterItem/1.0",
        "query": "customMetrics | where name == 'discount_amount' | summarize avg(value), max(value), min(value) by bin(timestamp, 1h)",
        "title": "Discount Amount (Avg/Max/Min per Hour)",
        "queryType": 0,
        "resourceType": "microsoft.insights/components",
        "visualization": "timechart"
      }
    },
    {
      "type": 3,
      "content": {
        "version": "KqlParameterItem/1.0",
        "query": "customMetrics | where name == 'discount_amount' | summarize TotalDiscount=sum(value) by bin(timestamp, 1d)",
        "title": "Total Discounts Applied (Daily)",
        "queryType": 0,
        "resourceType": "microsoft.insights/components",
        "visualization": "areachart"
      }
    }
  ]
}
