SELECT MediaDimension.mediaTitle, MediaDimension.mediaType, MediaDimension.mediaYear, ServiceDimension.serviceName
              FROM MediaDimension, ServiceDimension, MediaServiceFact
              WHERE MediaDimension.mediaKey = MediaServiceFact.MSmediaKey
              AND ServiceDimension.serviceKey = MediaServiceFact.MSserviceKey
              AND 1609384128 - MediaServiceFact.MSTimeStamp < 600000
              AND MediaDimension.mediaTitle LIKE '%Grinch%';
