SELECT COUNT(*) as "# of Logs"
	FROM LogHistory
	GROUP BY logHistoryStreamingKey
	LIMIT 1