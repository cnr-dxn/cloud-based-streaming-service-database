SELECT MediaDimension.mediaTitle, MediaDimension.mediaType, MediaDimension.mediaYear, ServiceDimension.serviceName
              FROM MediaDimension, ServiceDimension, MediaServiceFact
              WHERE MediaDimension.mediaKey = MediaServiceFact.MSmediaKey
              AND ServiceDimension.serviceKey = MediaServiceFact.MSserviceKey
              AND 1609887118- MediaServiceFact.MSTimeStamp < 3600
              AND MediaDimension.mediaTitle LIKE '%Firefly%';
