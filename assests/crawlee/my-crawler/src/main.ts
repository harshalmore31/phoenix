import { PlaywrightCrawler } from 'crawlee';
import axios from 'axios';
import pdfParse from 'pdf-parse';

const crawler = new PlaywrightCrawler({
    async requestHandler({ request, pushData, log }) {
        log.info(`Processing PDF from URL: ${request.url}`);

        try {
            // Download the PDF file
            const response = await axios.get(request.url, {
                responseType: 'arraybuffer', // Ensure the response is a binary buffer
            });

            // Parse the PDF content
            const pdfData = await pdfParse(response.data);
            const pdfText = pdfData.text; // Extract text content from the PDF

            // Save the extracted data
            await pushData({ url: request.url, content: pdfText });
            log.info(`Extracted content from PDF: ${request.url}`);
        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
            log.error(`Failed to process PDF at ${request.url}: ${errorMessage}`);
        }
    },

    // Optional settings for headless browsing
    maxRequestsPerCrawl: 5,
});

// Run the crawler with the PDF URL
await crawler.run([
    'https://file.notion.so/f/f/08d6bfe6-fb55-48d0-9cf2-aadb69e534ef/155ec8db-a316-47ae-b551-43779c405f3d/Qdrant-RAG-Evaluation-Guide-Best-Practices.pdf?table=block&id=1587b5c6-5e9c-8060-b302-d87f5cc72deb&spaceId=08d6bfe6-fb55-48d0-9cf2-aadb69e534ef&expirationTimestamp=1734336000000&signature=x975avnWmVRovrcQS4JUFsy0PYSIdv7DSpjyqB5JvLg&downloadName=Qdrant-RAG-Evaluation-Guide-Best-Practices.pdf',
]);

// Export the results to a file or process them as needed
await crawler.exportData('./result.json');
