cmake_minimum_required(VERSION 3.22)
project(lola)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)

# Check if the necessary source files exist
set(SOURCE_FILES
  Completions/BashCompletionsGenerator.swift
  Completions/CompletionsGenerator.swift
  Completions/FishCompletionsGenerator.swift
  Completions/ZshCompletionsGenerator.swift

  "Parsable Properties/Argument.swift"
  "Parsable Properties/ArgumentHelp.swift"
  "Parsable Properties/CompletionKind.swift"
  "Parsable Properties/Errors.swift"
  "Parsable Properties/Flag.swift"
  "Parsable Properties/NameSpecification.swift"
  "Parsable Properties/Option.swift"
  "Parsable Properties/OptionGroup.swift"

  "Parsable Types/CommandConfiguration.swift"
  "Parsable Types/EnumerableFlag.swift"
  "Parsable Types/ExpressibleByArgument.swift"
  "Parsable Types/ParsableArguments.swift"
  "Parsable Types/ParsableArgumentsValidation.swift"
  "Parsable Types/ParsableCommand.swift"

  Parsing/ArgumentDecoder.swift
  Parsing/ArgumentDefinition.swift
  Parsing/ArgumentSet.swift
  Parsing/CommandParser.swift
  Parsing/InputOrigin.swift
  Parsing/Name.swift
  Parsing/Parsed.swift
  Parsing/ParsedValues.swift
  Parsing/ParserError.swift
  Parsing/SplitArguments.swift

  Usage/HelpCommand.swift
  Usage/HelpGenerator.swift
  Usage/MessageInfo.swift
  Usage/UsageGenerator.swift

  Utilities/SequenceExtensions.swift
  Utilities/StringExtensions.swift
  Utilities/Tree.swift)

# Filter out missing files
foreach(file ${SOURCE_FILES})
  if(NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${file}")
    message(WARNING "File ${file} does not exist.")
    list(REMOVE_ITEM SOURCE_FILES ${file})
  endif()
endforeach()

# Add library only if there are source files
if(SOURCE_FILES)
  add_library(ArgumentParser ${SOURCE_FILES})

  target_compile_options(ArgumentParser PRIVATE $<$<BOOL:${BUILD_TESTING}>:-enable-testing>)
  target_link_libraries(ArgumentParser PRIVATE $<$<NOT:$<PLATFORM_ID:Darwin>>:Foundation>)

  set_property(GLOBAL APPEND PROPERTY ArgumentParser_EXPORTS ArgumentParser)
else()
  message(FATAL_ERROR "No source files found for ArgumentParser")
endif()

# Add executable
add_executable(main main.cpp)
set_target_properties(main PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
target_link_libraries(main PRIVATE ArgumentParser)

# Installation command
install(TARGETS main DESTINATION bin)
