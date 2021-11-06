SELECT serviceName as "Service", AVG(logHistoryTimeTaken) as "Average Time Taken (in seconds)"
	FROM LogHistory, ServiceDimension
	WHERE LogHistory.logHistoryStreamingKey = ServiceDimension.serviceKey
	GROUP BY serviceName
	ORDER BY AVG(logHistoryTimeTaken) DESC
