SELECT serviceName as "Service", AVG(logHistoryQuantity) as "Average Log Quantity"
	FROM LogHistory, ServiceDimension
	WHERE LogHistory.logHistoryStreamingKey = ServiceDimension.serviceKey
	GROUP BY serviceName
	ORDER BY AVG(logHistoryQuantity) DESC