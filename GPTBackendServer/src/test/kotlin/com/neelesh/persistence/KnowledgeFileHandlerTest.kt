package com.neelesh.persistence

import arrow.core.right
import com.neelesh.model.KnowledgeFile
import com.neelesh.routes.SimpleKnowledgeFileCreationRequest
import com.neelesh.util.UUIDGenerator
import io.mockk.every
import io.mockk.mockk
import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.Test

class KnowledgeFileHandlerTest {

    val knowledgeFileStore = mockk<KnowledgeFileStore>()
    val uuidGenerator = mockk<UUIDGenerator>()
    val knowledgeFileHandler = KnowledgeFileHandler(knowledgeFileStore, uuidGenerator)

    @Test
    fun `will create new knoweldge file`() {
        val simpleKnowledgeFileCreationRequest = SimpleKnowledgeFileCreationRequest(
            "knowledgeFileName",
            "someEmail"
        )

        every { uuidGenerator.get() } returns "someId"
        val expectedKnowledgeFile = KnowledgeFile(
            "someId",
            "someEmail",
            "knowledgeFileName",
            emptyList(),
            "{}"
        )
        every { knowledgeFileStore.saveKnowledgeFile(expectedKnowledgeFile) } returns expectedKnowledgeFile.right()

        val id = knowledgeFileHandler.create(simpleKnowledgeFileCreationRequest)

        Assertions.assertEquals("someId".right(), id)

    }

}