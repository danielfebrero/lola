cmake_minimum_required(VERSION 3.22)
project(lola)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)

# Add source files
add_library(ArgumentParser
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

# Example of set_target_properties
set_target_properties(main.cpp PROPERTIES RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin")
target_compile_options(ArgumentParser PRIVATE $<$<BOOL:${BUILD_TESTING}>:-enable-testing>)
target_link_libraries(ArgumentParser PRIVATE $<$<NOT:$<PLATFORM_ID:Darwin>>:Foundation>)

# Installation command
install(TARGETS main.cpp DESTINATION bin)

set_property(GLOBAL APPEND PROPERTY ArgumentParser_EXPORTS ArgumentParser)
