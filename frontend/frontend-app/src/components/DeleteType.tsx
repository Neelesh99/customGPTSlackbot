import {Dialog, Transition} from '@headlessui/react'
import {Fragment, useContext, useState} from 'react'
import {SimpleKnowledgeFileDeletionRequest} from "../model/StorageModel";
import {ChosenKnowledgeFileContext} from "../service/ChosenKnowledgeFileContext";
import {AuthenticationContext} from "../service/AuthenticationContext";
import {EnvironmentContext} from "../service/EnvironmentContext";
import {sendDeleteKnowledgeFile} from "../service/DeleteService";

export default function DeleteType() {
    const [isOpen, setIsOpen] = useState(false)
    const targetFile = useContext(ChosenKnowledgeFileContext)
    const user = useContext(AuthenticationContext)
    const environment = useContext(EnvironmentContext)
    function closeModal() {
        setIsOpen(false)
    }

    function openModal() {
        const deletionRequest: SimpleKnowledgeFileDeletionRequest = {
            knowledgeFileId: targetFile.id,
            email: user.email
        }
        void sendDeleteKnowledgeFile(environment.backendPrefix, deletionRequest)
        setIsOpen(true)
    }

    return (
        <>
            <div className="px-2">
                <button
                    type="button"
                    onClick={openModal}
                    className="rounded-md bg-black bg-opacity-20 px-4 py-2 text-sm font-medium text-white hover:bg-opacity-30 focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75"
                >
                    Delete
                </button>
            </div>

            <Transition appear show={isOpen} as={Fragment}>
                <Dialog as="div" className="relative z-10" onClose={closeModal}>
                    <Transition.Child
                        as={Fragment}
                        enter="ease-out duration-300"
                        enterFrom="opacity-0"
                        enterTo="opacity-100"
                        leave="ease-in duration-200"
                        leaveFrom="opacity-100"
                        leaveTo="opacity-0"
                    >
                        <div className="fixed inset-0 bg-black bg-opacity-25" />
                    </Transition.Child>

                    <div className="fixed inset-0 overflow-y-auto">
                        <div className="flex min-h-full items-center justify-center p-4 text-center">
                            <Transition.Child
                                as={Fragment}
                                enter="ease-out duration-300"
                                enterFrom="opacity-0 scale-95"
                                enterTo="opacity-100 scale-100"
                                leave="ease-in duration-200"
                                leaveFrom="opacity-100 scale-100"
                                leaveTo="opacity-0 scale-95"
                            >
                                <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all">
                                    <Dialog.Title
                                        as="h3"
                                        className="text-lg font-medium leading-6 text-gray-900"
                                    >
                                        Submission succesfull
                                    </Dialog.Title>
                                    <div className="mt-2">
                                        <p className="text-sm text-gray-500">
                                            This information has now been submitted, we will index it to the knowledge file you set.
                                        </p>
                                    </div>

                                    <div className="mt-4">
                                        <button
                                            type="button"
                                            className="inline-flex justify-center rounded-md border border-transparent bg-blue-100 px-4 py-2 text-sm font-medium text-blue-900 hover:bg-blue-200 focus:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
                                            onClick={closeModal}
                                        >
                                            Got it, thanks!
                                        </button>
                                    </div>
                                </Dialog.Panel>
                            </Transition.Child>
                        </div>
                    </div>
                </Dialog>
            </Transition>
        </>
    )
}
