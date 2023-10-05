// Grade.sol
// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.19;

contract GradeStorage {
    struct ScoreRecord {
        uint256[] scores;
        string[] subjects;
        string[] reasons;
        uint256[] blockTimestamps;
        string[] teacherIds;
    }

    mapping(string => ScoreRecord) private scores;

    function updateScore(string memory studentId, uint256 newScore, string memory subject, string memory reason, string memory teacherId) public {
        ScoreRecord storage record = scores[studentId];
        record.scores.push(newScore);
        record.subjects.push(subject);
        record.reasons.push(reason);
        record.blockTimestamps.push(block.timestamp);
        record.teacherIds.push(teacherId);

        emit ScoreUpdated(studentId, subject, record.scores, record.subjects, record.reasons, record.blockTimestamps, record.teacherIds);
    }

    function getScore(string memory studentId) public view returns (uint256[] memory, string[] memory, string[] memory, uint256[] memory, string[] memory) {
        ScoreRecord storage record = scores[studentId];
        return (record.scores, record.subjects, record.reasons, record.blockTimestamps, record.teacherIds);
    }

    event ScoreUpdated(string indexed studentId, string subject, uint256[] scores, string[] subjects, string[] reasons, uint256[] blockTimestamps, string[] teacherIds);
}